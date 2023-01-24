# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# print(spacex_df.head())
# print(spacex_df['Launch Site'].unique())
print(spacex_df.columns)

# Create a dash application
app = dash.Dash(__name__)

launch_sites = spacex_df['Launch Site'].unique()
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', options=dropdown_options, value='ALL', placeholder='Select launch site'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                marks={0: '0', 100: '100'},
                                                value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):


    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
        names='Launch Site',
        title='success launches by site')
        return fig
    else:
        data = spacex_df[spacex_df['Launch Site'] == entered_site]
        s = data['class']
        fig = px.pie(s, values=s.value_counts().values,
                     names=s.value_counts().index,
                     title=f'launches for site {entered_site}')
        return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, slider_value):

    data = spacex_df[spacex_df['Payload Mass (kg)'] >= slider_value[0]]
    data = data[data['Payload Mass (kg)'] <= slider_value[1]]

    if entered_site == 'ALL':
        fig = go.Figure(data=go.Scatter(y=data['class'], x=data['Payload Mass (kg)'], mode='markers', marker=dict(color='green')))
        return fig
    else:
        data2 = data[data['Launch Site'] == entered_site]
        fig = go.Figure(data=go.Scatter(y=data2['class'], x=data2['Payload Mass (kg)'], mode='markers', marker=dict(color='green')))
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
