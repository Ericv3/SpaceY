# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create app layout
app.layout = html.Div(children=[

    # Title
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # TASK 1: Dropdown for Launch Site Selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie chart
    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.Br(),

    # Payload slider text
    html.P("Payload range (Kg):"),

    # TASK 3: Payload Range Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={
            0: '0',
            2500: '2500',
            5000: '5000',
            7500: '7500',
            10000: '10000'
        },
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Scatter chart
    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')
    )

])

# TASK 2:
# Callback for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):

    # Case when ALL sites are selected
    if entered_site == 'ALL':

        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )

        return fig

    # Case when a specific site is selected
    filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]

    fig = px.pie(
        filtered_df,
        names='class',
        title=f'Success vs Failed Launches for {entered_site}'
    )

    return fig


# TASK 4:
# Callback for scatter chart
@app.callback(
    Output(component_id='success-payload-scatter-chart',
           component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(entered_site, payload_range):

    low, high = payload_range

    # Filter dataframe by payload range
    mask = (
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    )

    filtered_df = spacex_df[mask]

    # ALL sites selected
    if entered_site == 'ALL':

        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation Between Payload and Success for All Sites'
        )

        return fig

    # Specific site selected
    site_df = filtered_df[
        filtered_df['Launch Site'] == entered_site
    ]

    fig = px.scatter(
        site_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=f'Correlation Between Payload and Success for {entered_site}'
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)