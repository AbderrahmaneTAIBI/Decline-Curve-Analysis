import base64
import io
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
load_figure_template('LUX')
from scipy.optimize import curve_fit

# Define the Arp's equations for oil production
def exponential(t, qi, di):
    return qi * np.exp(-di * t)

def hyperbolic(t, qi, di, b):
    return qi / (1 + b * di * t) ** (1 / b)

def harmonic(t, qi, di):
    return qi / (1 + di * t)

def stretched_exponential(t, qi, di, beta):
    return qi * np.exp(-(di * t) ** beta)

# Load the synthetic decline curves from the CSV file
df = pd.read_csv('/Users/macbookpro/Desktop/LinkedIn Work/LinkedIn Posts/Visualisations Projects/Decline Curve Analysis/synthetic_decline_curves.csv', index_col=0, parse_dates=True)

# Define the app
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])

# Define the layout
app.layout = html.Div([
    html.H1("Decline Curve Analysis", style={"text-align": "center"}),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div([
        html.Label("Select a well", style={'margin-right': '10px'}),
        dcc.Dropdown(
            id='well-dropdown',
            options=[{'label': well, 'value': well} for well in df.columns],
            value=df.columns[0],
            clearable=False,
            style={'width': '200px', 'margin-right': '10px'}
        ),
        html.Label("Select a decline model", style={'margin-right': '10px'}),
        dcc.Dropdown(
            id='model-dropdown',
            options=[
                {'label': 'Exponential', 'value': 'exponential'},
                {'label': 'Hyperbolic', 'value': 'hyperbolic'},
                {'label': 'Harmonic', 'value': 'harmonic'},
                {'label': 'Stretched Exponential', 'value': 'stretched_exponential'}
            ],
            value='exponential',
            clearable=False,
            style={'width': '200px', 'margin-right': '10px'}
        ),
    ], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
    dcc.Graph(id='production-graph'),
    html.Div(id='mse-output', style={'text-align': 'center', 'margin-top': '10px'})
])



# Define the callback function
@app.callback(
    [Output('production-graph', 'figure'), Output('mse-output', 'children')],
    [Input('well-dropdown', 'value'), Input('model-dropdown', 'value'), Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_graph(well, model, contents, filename):
    try:
        # Use the pre-loaded data if no file was uploaded
        df = pd.read_csv('/Users/macbookpro/Desktop/LinkedIn Work/LinkedIn Posts/Visualisations Projects/Decline Curve Analysis/synthetic_decline_curves.csv', index_col=0, parse_dates=True)
    except FileNotFoundError:
        return dash.no_update, dash.no_update

    if contents is not None:
        # Read the uploaded data into a Pandas DataFrame
        content_type, content_string = contents[0].split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename[0]:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename[0]:
                # Assume that the user uploaded an Excel file
                df = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            return dash.no_update, dash.no_update

    # Get the production data for the selected well
    data = df[well].dropna()

    # Extract the time (days) and production rate (STB/d) arrays
    time = data.index.to_numpy().astype('float')
    production = data.to_numpy()

    # Fit the selected decline model to the selected well's data and compute the MSE
    if model == 'exponential':
        params, cov = curve_fit(exponential, time, production, p0=[production[0], 0.1])
        fit = exponential(time, *params)
        mse = np.mean((fit - production) ** 2)
    elif model == 'hyperbolic':
        params, cov = curve_fit(hyperbolic, time, production, p0=[production[0], 0.1, 1])
        fit = hyperbolic(time, *params)
        mse = np.mean((fit - production) ** 2)
    elif model == 'harmonic':
        params, cov = curve_fit(harmonic, time, production, p0=[production[0], 0.1, 1])
        fit = harmonic(time, *params)
        mse = np.mean((fit - production) ** 2)
    elif model == 'stretched_exponential':
        params, cov = curve_fit(stretched_exponential, time, production, p0=[production[0], 0.1, 1])
        fit = stretched_exponential(time, *params)
        mse = np.mean((fit - production) ** 2)

    # Generate the production graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time, y=production, mode='markers', name='Production data'))
    fig.add_trace(go.Scatter(x=time, y=fit, mode='lines', name='Model fit'))

    # Format the production graph
    fig.update_layout(title=f'{well} Production Data and {model.title()} Decline Model Fit',
                      xaxis_title='Time (days)',
                      yaxis_title='Production Rate (STB/d)')

    # Generate the MSE output
    mse_output = f'Mean Squared Error: {mse:.2f}'

    return fig, mse_output


if __name__ == "__main__":
    app.run_server(debug=True)