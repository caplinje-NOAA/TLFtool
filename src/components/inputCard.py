# -*- coding: utf-8 -*-
"""
Created on Sun May  7 08:39:35 2023
The general options (top-left card) components and primary callback of the app
@author: jim
"""

# dash imports
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

# data science imports
import pandas as pd

# project imports
from . import ids, plots
from ..dataHandling import tableData

# data to initialize the app
startingData = tableData.getExData('OSW example 1')

### Components ###
# radio for selecting example or user input
dataTypeRadio = dbc.RadioItems(['Example Data','User Data'], 'Example Data', inline=True, id=ids.DTYPE_RADIO,className = 'radio-item')

# dropdown to select different example data
exampleDataDropdown = dcc.Dropdown(['OSW example 1', 'OSW example 2', 'OSW example 3', 'User example'], 'OSW example 1', id=ids.EX_DATA_DROPDOWN, searchable=False,clearable=False,className= 'dropdown')

# input group for number of rows
rowsInput = dbc.InputGroup(
            [
                dbc.InputGroupText('data rows',className='input-group-label'),
                dbc.Input(type="number",id=ids.DATA_ROWS_INPUT,value=3,min=2,max=100,step=1),
                dbc.InputGroupText(''),
            ],
            className="mb-3",
        )

dataTable = dash_table.DataTable(
            id=ids.DATA_TABLE,
            columns=([{'id': 'range_m', 'name': 'Range (m)'}] +
                     [{'id': 'level', 'name': 'Level (dB)'}]
                     
            
            ),
            data=startingData,
            style_cell={'textAlign': 'center'},
                
            
            editable=True
        )

metricDropdown = html.Div([
    html.H5('Sound Metric'),
    dcc.Dropdown(['SPL', 'SEL', 'Peak'], 'SPL', id=ids.METRIC_DROPDOWN, searchable=False,clearable=False,className= 'dropdown')
      ]  
)
        


# Full input card
card = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("Data Inputs", className="card-title"),
                dataTypeRadio,
                dbc.Collapse(children=[
                metricDropdown,
                rowsInput], id=ids.USER_DATA_COLLAPSE, is_open=False),
                dbc.Collapse(exampleDataDropdown,id=ids.EX_DATA_COLLAPSE, is_open=True),
                dataTable,
   
                
                
        
            ]
        ),
    ],
    style={"width": "100%"},
)




def render(app: Dash) -> html.Div:
    @app.callback(
        output = Output(ids.DATA_TABLE,'data',allow_duplicate=True),
        inputs = Input(ids.DATA_ROWS_INPUT,'value'),
        state = State(ids.DATA_TABLE,'data')
        )
    def adjustRows(n,data):
 
        if n>len(data):
            data.append({'range_m':100,'level':150})
        else:
            data = data[0:-1]
        
        return data   

    @app.callback(
        output = Output(ids.LIN_PLOT,'figure',allow_duplicate=True),
        inputs = Input(ids.DATA_TABLE,'data'),
        
      
        )
    def updatePlot(data):
        df = pd.DataFrame(data = data,dtype=float)

        return plots.plotInputs(df)
    
    @app.callback(
    Output(ids.EX_DATA_COLLAPSE, "is_open"),
    Output(ids.USER_DATA_COLLAPSE, "is_open"),
    Output(ids.EX_DATA_DROPDOWN,'value'),
  
      
    Input(ids.DTYPE_RADIO, "value"),
    )
    def toggle_collapse(dataType):
      
        if dataType=='Example Data':
            return True,False,'OSW example 1'
        
        if dataType=='User Data':
            return False,True,'User example'

    @app.callback(
        Output(ids.DATA_TABLE, "data",allow_duplicate=True),
        Input(ids.EX_DATA_DROPDOWN,'value'),
        
      
        )
    def updateExData(example):
        data = tableData.getExData(example)
    

        return data                
      
        



    return html.Div(
        [
            card
            
        ]
    )


