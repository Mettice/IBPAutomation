from flask import Flask, render_template, request, redirect, url_for, flash
import plotly.express as px
import plotly.utils
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
from src.utils.data_fetcher import DataFetcher
from src.utils.outcome_tracker import OutcomeTracker
from src.ml.forecaster import SalesForecaster
from src.ml.anomaly_detector import AnomalyDetector
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)



print("Current working directory:", os.getcwd())
print("Contents of current directory:", os.listdir())
print("Contents of templates directory:", os.listdir('templates'))
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

def convert_numpy_types(obj):
    if isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

def analyze_data(data):
    print("In analyze_data - Type of data:", type(data))
    print("In analyze_data - Shape of data:", data.shape if hasattr(data, 'shape') else "No shape attribute")
    print("In analyze_data - First few rows of data:", data[:5] if isinstance(data, np.ndarray) else data.head())

    # Ensure data is a DataFrame
    if isinstance(data, np.ndarray):
        data = pd.DataFrame(data, columns=['Date', 'Sales', 'Customer_Satisfaction'])
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)
    elif not isinstance(data, pd.DataFrame):
        raise ValueError(f"Unexpected data type: {type(data)}")

    # Forecast sales
    forecaster = SalesForecaster()
    forecaster.train(data)
    future_dates = pd.date_range(start=data.index[-1], periods=30)
    forecasted_sales = forecaster.forecast(future_dates)

    # Detect anomalies
    detector = AnomalyDetector()
    data_with_anomalies = detector.detect_anomalies(data)

    # Get target results
    tracker = OutcomeTracker(data)
    results = tracker.check_targets()
    results = {k: convert_numpy_types(v) for k, v in results.items()}

    return forecasted_sales, data_with_anomalies, results


def create_charts(data, forecasted_sales, data_with_anomalies):
    sales_chart = px.line(data, x=data.index, y='Sales', title='Sales Over Time')
    satisfaction_chart = px.line(data, x=data.index, y='Customer_Satisfaction', title='Customer Satisfaction Over Time')
    forecast_chart = px.line(pd.DataFrame({'Date': forecasted_sales.index, 'Forecasted_Sales': forecasted_sales}),
                             x='Date', y='Forecasted_Sales', title='Sales Forecast')
    anomaly_chart = px.scatter(data_with_anomalies, x=data_with_anomalies.index, y='Sales',
                               color='Anomaly', title='Sales Anomalies',
                               color_discrete_map={1: 'blue', -1: 'red'})

    charts_json = {
        'sales_chart': json.dumps(sales_chart, cls=plotly.utils.PlotlyJSONEncoder),
        'satisfaction_chart': json.dumps(satisfaction_chart, cls=plotly.utils.PlotlyJSONEncoder),
        'forecast_chart': json.dumps(forecast_chart, cls=plotly.utils.PlotlyJSONEncoder),
        'anomaly_chart': json.dumps(anomaly_chart, cls=plotly.utils.PlotlyJSONEncoder)
    }
    return charts_json


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    fetcher = DataFetcher()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    symbol = request.args.get('symbol', default='MSFT')

    try:
        data = fetcher.fetch_data(symbol, start_date, end_date)
        print("Type of data after fetch:", type(data))
        print("Shape of data:", data.shape if hasattr(data, 'shape') else "No shape attribute")
        print("First few rows of data:", data[:5] if isinstance(data, np.ndarray) else data.head())

        processed_data = fetcher.preprocess_data(data)
        print("Type of processed_data:", type(processed_data))
        print("Shape of processed_data:",
              processed_data.shape if hasattr(processed_data, 'shape') else "No shape attribute")
        print("First few rows of processed_data:",
              processed_data[:5] if isinstance(processed_data, np.ndarray) else processed_data.head())

        # Convert numpy array to pandas DataFrame if necessary
        if isinstance(processed_data, np.ndarray):
            processed_data = pd.DataFrame(processed_data, columns=['Date', 'Sales', 'Customer_Satisfaction'])
            processed_data['Date'] = pd.to_datetime(processed_data['Date'])
            processed_data.set_index('Date', inplace=True)

        print("Final type of processed_data:", type(processed_data))
        print("Final shape of processed_data:", processed_data.shape)
        print("Final first few rows of processed_data:", processed_data.head())

        forecasted_sales, data_with_anomalies, results = analyze_data(processed_data)
        charts_json = create_charts(processed_data, forecasted_sales, data_with_anomalies)

        return render_template('dashboard.html',
                               charts=charts_json,
                               results=results,
                               symbol=symbol,
                               error=None)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())
        return render_template('dashboard.html',
                               charts={},
                               results={},
                               symbol=symbol,
                               error=str(e))

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print("Current working directory:", os.getcwd())
    print("Template folder:", app.template_folder)
    print("Files in template folder:", os.listdir(app.template_folder))

    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                return redirect(url_for('map_columns', filename=filename))
        return render_template('upload.html')
    except Exception as e:
        print(f"Error in upload_file: {str(e)}")
        return str(e), 500


def map_columns(filename):
    if request.method == 'POST':
        column_mapping = {
            'Date': request.form['date_column'],
            'Sales': request.form['sales_column'],
            'Customer_Satisfaction': request.form['satisfaction_column']
        }
        return redirect(url_for('analyze', filename=filename, mapping=json.dumps(column_mapping)))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    columns = pd.read_csv(file_path, nrows=0).columns.tolist()
    return render_template('map_columns.html', columns=columns, filename=filename)


@app.route('/analyze/<filename>')
def analyze(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    column_mapping = json.loads(request.args.get('mapping'))

    data = pd.read_csv(file_path)
    data = data.rename(columns=column_mapping)
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values('Date')
    data.set_index('Date', inplace=True)

    forecasted_sales, data_with_anomalies, results = analyze_data(data)
    charts_json = create_charts(data, forecasted_sales, data_with_anomalies)

    return render_template('dashboard.html',
                           charts=charts_json,
                           results=results,
                           symbol="Custom Data",
                           error=None)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv', 'xlsx'}


if __name__ == '__main__':
    app.run(debug=True)