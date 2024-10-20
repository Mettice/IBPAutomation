from flask import Flask, render_template
import plotly.express as px
import plotly.utils
import json
import numpy as np
from src.utils.data_utils import create_realistic_mock_data
from src.utils.outcome_tracker import OutcomeTracker

app = Flask(__name__)

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

@app.route('/')
def dashboard():
    # Fetch latest data and results
    data = create_realistic_mock_data()
    tracker = OutcomeTracker(data)
    results = tracker.check_targets()

    # Convert NumPy types to Python native types
    results = {k: convert_numpy_types(v) for k, v in results.items()}

    # Create visualizations
    sales_chart = px.line(data, x='Date', y=['Product_A_Units', 'Product_B_Units', 'Product_C_Units'])
    satisfaction_chart = px.line(data, x='Date', y='Customer_Satisfaction')

    # Convert charts to JSON for rendering in HTML
    sales_chart_json = json.dumps(sales_chart, cls=plotly.utils.PlotlyJSONEncoder)
    satisfaction_chart_json = json.dumps(satisfaction_chart, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html',
                           sales_chart=sales_chart_json,
                           satisfaction_chart=satisfaction_chart_json,
                           results=results)

if __name__ == '__main__':
    app.run(debug=True)