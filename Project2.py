# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 21:45:31 2023

@author: NQing
"""

import dash
from dash import html as html
from dash import dcc as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


#getting the dataset

pro = pd.read_csv('https://raw.githubusercontent.com/quynhnhu12345678910/project2/main/Coffee_Chain.csv')

#dash app

app = dash.Dash(__name__)
server=app.server
#layout
app.layout = html.Div(children = [
    html.Div([
        html.H1(children = 'Coffee Chain Dashboard',
                style={'text-align': 'center', 'font-size': '36px', 'color': '#333333', 'margin': '10px'})
    ]),
    html.Div([
        html.Div([
            dcc.Checklist(
                id = 'geo-checklist',
                options = [{'label': i, 'value': i}
                           for i in pro['Product_type'].unique()],
                value = ["Coffee"],
                labelStyle={'display': 'block', 'margin': '10px'}
            ),
            dcc.Dropdown(
                id='state-dropdown',
                options=[{'label': i, 'value': i} for i in pro['State'].unique()],
                value=[],
                multi=True,
                placeholder='Select states'
            ),
            dcc.Graph(id = 'price-graph'),
            
        ], className='six columns', style={'border': '1px solid #ced4da', 'border-radius': '5px', 'margin': '10px'}),
        html.Div([
            dcc.Graph(id = 'scatter-chart')
        ], className='six columns', style={'border': '1px solid #ced4da', 'border-radius': '5px', 'margin': '10px'})
    ], className='row')
])

@app.callback(
    Output(component_id = 'price-graph', component_property ='figure'),
    Input(component_id = 'geo-checklist', component_property = 'value'),
    Input(component_id = 'state-dropdown', component_property = 'value')
)
def update_bar(selected_departments, selected_states):
    data = pro[pro['Product_type'].isin(selected_departments)]
    if selected_states:
        data = data[data['State'].isin(selected_states)]
    bar = px.histogram(data, x ='State', nbins=30, color_discrete_sequence=['green'])
    bar.update_layout(plot_bgcolor='#f8f8f8', paper_bgcolor='#f8f8f8',
                      font_color='#333333', title_font_size=30,
                      xaxis_title='State', yaxis_title='Count')
    return bar

@app.callback(
    Output(component_id = 'scatter-chart', component_property ='figure'),
    Input(component_id = 'geo-checklist', component_property = 'value'),
    Input(component_id = 'state-dropdown', component_property = 'value')
)
def update_scatter(selected_departments, selected_states):
    data = pro[pro['Product_type'].isin(selected_departments)]
    if selected_states:
        data = data[data['State'].isin(selected_states)]
    graph = px.scatter(data, x ='Budget_sales', y = 'Budget_profit', color_discrete_sequence=['#FF5733', '#FFC300', '#C70039', '#900C3F', '#581845'])
    return graph

if __name__ == '__main__':
    app.run_server(debug = True)
