# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 17:30:28 2021

@author: hatti
"""

"""
Dashboard created in lecture Week 11
"""

"""
Dash template
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_table

stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# pandas dataframe to html table
'''
def generate_table(dataframe, max_rows=2000):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
'''
app = dash.Dash(__name__, external_stylesheets=stylesheet)

PAGE_SIZE =22

df = pd.read_pickle('covidproject.pkl')

app.layout = html.Div([
    html.H1('US Most Populous States Covid19 Cases and Vaccinations',style={'textAlign' : 'center'}),
    html.Br(),

    html.Div([html.H5("Multi-Dropdown: "),
              dcc.Dropdown(options=[{'label': 'California', 'value': 'CA'},
                           {'label': 'Texas', 'value': 'TX'},
                           {'label': 'Florida', 'value': 'FL'},
                           {'label': 'New York State', 'value': 'NY'},
                           {'label': 'Pennsylvania', 'value': 'PA'},
                           {'label': 'Illinois', 'value': 'IL'},
                           {'label': 'Ohio', 'value': 'PA'},
                           {'label': 'Georgia', 'value': 'GA'},
                           {'label': 'North Carolina', 'value': 'NC'},
                           {'label': 'Michigan', 'value': 'MI'},
                           {'label': 'Massachusetts', 'value': 'MA'}],
                           id='states_multidropdown',
                           value=['CA','MA'],
                           multi=True),
              html.Br(),
              html.H5("Select Fields: "),
              dcc.RadioItems(options=[{'label': 'New Cases', 'value': 'Nc'},
                                      {'label': 'Vaccinations', 'value': 'Vc'}],
                             id='field-radioitems',
                             value='Nc'),
              html.Br(),
              html.Br(),
              html.Br()],
             
             style= {'width': '49%','float' : 'left','display': 'inline-block'}
          
             ),

           
    html.Div([
    #html.H5("Slider: "),
             dash_table.DataTable(
                            id='table-multicol-sorting',
                            columns=[
                                {"name": i, "id": i} for i in sorted(df.columns)
                            ],
                            #data=df.to_dict('records'),
                            page_current=0,
                            page_size=PAGE_SIZE,
                            page_action='native',  
                            sort_action='native',

                            sort_mode='multi',

                            sort_by=[]
                        )
            ],
            #html.Div(
            #id='table_my'),
        style = {'width': '49%','float' : 'right'}
        )
    ])




@app.callback(
    Output('table-multicol-sorting', 'data'),
    Input("states_multidropdown",'value'))

def update_table(states_multidropdown):
    if states_multidropdown is None or states_multidropdown == []:
        states_multidropdown = list(set(df.Location))
    dff = df[df['Location'].isin(states_multidropdown)]
    return dff.to_dict('records')



if __name__ == '__main__':
    app.run_server(debug=True)
    

