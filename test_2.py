# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 21:55:34 2021

@author: hatti
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_table
from datetime import date,timedelta
from calendar import monthrange


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] 
datableapp = dash.Dash(__name__, external_stylesheets=stylesheet)

PAGE_SIZE =22

df = pd.read_pickle('covidproject.pkl')
statelabels = [{'label' : state, 'value' : state} for state in set(df.State)]
yLabels = [{'label' : col, 'value' : col} for col in df.columns[2:6]]

df['Date'] = pd.to_datetime(df.Date).dt.date
'''
#get future one month later
today = date.today()
nextMd = date(today.year, today.month, monthrange(today.year, today.month)[1]) + timedelta(1)
nextMon = nextMd.strftime('%Y-%m')
dateRange = list(set([caseDT.strftime('%Y-%m')for caseDT in df.Date]))
dateRange.append(nextMon)
dates = sorted(dateRange)
date_mark = {i : dates[i] for i in range(0,len(dates))}
'''

cols = ['Date','State','New Case','New Death','Daily Vaccinations',
        'Daily Vaccinations/million']

#fig = px.scatter(df, x="Date", y='Daily Vaccinations', color='Location')
app.layout = html.Div([
    html.H1('US Most Populous States Covid19 Cases and Vaccinations',style={'textAlign' : 'center'}),
    html.Br(),

    html.Div([html.H5("Multi-Dropdown: "),
              dcc.Dropdown(options=statelabels,
                           id='states_multidropdown',
                           value=['California','Massachusetts'],
                           multi=True),
              html.Br(),
              html.H5("Select Fields: "),
              dcc.RadioItems(options = yLabels,
                             id='field_radioitems',
                             value='New Case',
                             labelStyle={'display': 'inline-block'}),
              #html.Br(),
              ],
             
             style= {'width': '49%','float' : 'left','display': 'inline-block'}
          
             ),

    html.Div([dcc.Graph(id='ts_fig')],
             style = {'width': '49%','display': 'inline-block','float':'right'}),      
    html.Div([
    #html.H5("Slider: "),
             dash_table.DataTable(
                            id='table-multicol-sorting',
                            columns=[
                                {"name": i, "id": i} for i in cols
                            ],
                                                    
                            style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Date', 'Region']
                            ],
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'
                                }
                            ],
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            },
                            style_cell=dict(textAlign='left'),
                            #data=df.to_dict('records'),
                            page_current=0,
                            page_size=PAGE_SIZE,
                            page_action='native',  
                            sort_action='native',
                            sort_mode='multi',
                            sort_by=[]
                        )
            ],
            #id='table_my',
        #style = {'width': '49%'}
        )
  ])

@app.callback(
    Output('table-multicol-sorting', 'data'),
    Output(component_id="ts_fig", component_property="figure"),
    [Input(component_id="states_multidropdown", component_property="value"),
    Input(component_id = 'field_radioitems',component_property = 'value')])

def update_fig_table(states,field):
    if states is None or states == []:
        states= list(set(df.State))
   # dff = df[(df.Date >= dates[0]) & (df.Date<=dates[-1])]
    df2 = df[df['State'].isin(states)].sort_values(by = 'Date')
    
    fig = px.scatter(df2, x='Date', y=field, color = 'State')
    fig.update_traces(mode='lines+markers',marker=dict(size=5))
    fig.update_layout(xaxis_rangeslider_visible=True)
    return df2.to_dict('records'),fig
    

   

if __name__ == '__main__':
    app.run_server(debug=True)
    



