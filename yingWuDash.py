# -*- coding: utf-8 -*-
'''
Created on Mon Apr 26 21:55:34 2021
'''

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

app = dash.Dash(__name__, external_stylesheets=stylesheet)

PAGE_SIZE =20

df = pd.read_pickle('covidproject.pkl')
statelabels = [{'label' : state, 'value' : state} for state in set(df.State)]
yLabels = [{'label' : col, 'value' : col} for col in df.columns[2:]]

df['Date'] = pd.to_datetime(df.Date).dt.date

cols = ['Date','State','Total Cases','New Case','New Death','Daily Vaccinations',
        'Daily Vaccinations/million']

app.layout = html.Div([
    html.H1('2021 Covid-19 Cases and Vaccinations in Populous US States',style={'fontFamily':'Helvetica','textAlign' : 'center','marginTop': 30}),

    html.Div([html.Label("Select a State/States: ",style={'textAlign' : 'center','paddingBottom':15}),
              dcc.Dropdown(options=statelabels,placeholder="Select a state/states",
                           id='states_multidropdown',
                           value=['California','Massachusetts'],
                           multi=True),
              html.Br(),
              html.Label("Select a Variable for the Graph: ",style={'textAlign' : 'center','paddingBottom':15}),
              dcc.RadioItems(options= yLabels,
                             id='field_radioitems',
                             value='New Case',
                             #labelStyle={'display': 'inline-block'}
                             style = {'border-radius': '5px','backgroundColor': 'rgb(255, 255, 255)'})
                             
              #html.Br(),
              ],
             
             style= {'width': '15%','float' : 'left','display': 'inline-block',
                     'marginTop': 70,
                     'backgroundColor': 'rgb(250, 250, 250)',                     
                     'padding': '20px 15px 160px 5px'
}
          
             ),
    html.Div([dcc.Graph(id='ts_fig',figure = {'layout': {'height': 600
            }})],
             style = {'width': '75%','display': 'inline-block','paddingLeft':'30px','paddingTop':'20px'}),      
    html.Div([
             dash_table.DataTable(
                            id='table-multicol-sorting',
                            columns=[
                                {"name": i, "id": i} for i in cols
                            ],
                            css=[{'selector': 'table', 'rule': 'table-layout: fixed'}],
                                style_cell={
                                    'width': '{}%'.format(len(df.columns)),
                                    'textOverflow': 'ellipsis',
                                    'overflow': 'hidden',
                                    'textAlign':'right'
                                    },
                            style_cell_conditional=[
                                {'if': {'column_id': 'Date'},
                                    'width': '50px'},
                                {'if': {'column_id': 'New Case'},
                                    'width': '50px'},
                                {'if': {'column_id': 'New Death'},
                                    'width': '30px'},
                                {'if': {'column_id': 'State'},
                                    'width': '40px'},
                                {'if': {'column_id': 'Daliy Vaccinations'},
                                    'width': '50px'},
                                
                                ],
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            },
                           # style_cell=dict(textAlign='left'),
                            #data=df.to_dict('records'),
                            page_current=0,
                            page_size=PAGE_SIZE,
                            page_action='native',  
                            sort_action='native',


                            sort_mode='multi',

                            sort_by=[]
                        )
            ]),
            
       html.Div(dcc.Markdown('''
                             ###### **Note**
                             - Data from this dashboard daily updates Covid-19 cases and vaccinations in 
                             Massachusetts and the top 10 most populous states of the US
                             - The graph shows the trend of Covid-19 cases and new doses of vaccinations admistered per day since 
                             the vaccine started to deploy nationwide on 2021/1/12
                             - "Daily_vaccinations/million" indicates the number of new doses of vaccinations per million people in the total 
                             population of the state received each day 
                             - Primary data source: [CDC](https://covid.cdc.gov/covid-data-tracker/#cases_casesper100klast7days)
                             and [Our World in Data](https://ourworldindata.org/us-states-vaccinations)
                             - References on customizing dashboard layout and CSS style:
                                     * https://dash.plotly.com/dash-html-components
                                     * https://www.w3schools.com/css/css_margin.asp
                                     
                                     
                            April 2021, Ying Wu
                             '''),
                             style= {'marginTop': '20px'}
                     )
                 ],
    
    style={'marginRight': 50, 'marginLeft': 50},
    
  )

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
    
    fig = px.scatter(df2, x='Date', y=field, color = 'State',template='ggplot2')
    fig.update_xaxes(showgrid=False)
    fig.update_traces(mode='lines+markers',marker=dict(size=5))
    fig.update_layout(title="A Time Series Plot on Covid-19 Cases and Vaccinations", 
                     font = dict(family="Arial, Helvetica, sans-serif",
        size=15),xaxis_rangeslider_visible=True)
    return df2.to_dict('records'),fig
    

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
    
