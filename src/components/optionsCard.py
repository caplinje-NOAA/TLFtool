# -*- coding: utf-8 -*-
"""
Created on Sun May  7 08:39:35 2023
The general options (top-left card) components and primary callback of the app
@author: jim
"""

# dash imports
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
#from dash.dependencies import Input, Output



# project imports
from . import ids



### input components

extrap_Input = dbc.InputGroup(
            [
                dbc.InputGroupText('Extrapolation Fraction',className='input-group-label'),
                dbc.Input(type="number",id=ids.EXTRAP_INPUT,value=0.25, min=0, max=.999,step=0.1),
                dbc.InputGroupText('frac.'),
            ],
            className="mb-3",
        )

confidence_Input = dbc.InputGroup(
            [
                dbc.InputGroupText('Confidence Interval',className='input-group-label'),
                dbc.Input(type="number",id=ids.CONF_INT_INPUT,value=95, min = 1, max = 99),
                dbc.InputGroupText('%'),
            ],
            className="mb-3",
        )

# Button for toggling transect collapse and plotting confidence intervals
showConfButton = dbc.Button(
                "Show Confidence Bands",
                id=ids.SHOW_CONF_BUTTON,
                className="button",
                color="primary",
                n_clicks=0,
                )

modelDropdown = html.Div([
    html.H5('model(s)'),
    dcc.Dropdown(['Geometric Spreading', 'Damped Geometric Spreading', 'Damped Cylindrical Spreading'], ['Geometric Spreading','Damped Geometric Spreading'], id=ids.MODEL_DROPDOWN, searchable=False,clearable=True,multi=True)
      ]  
)




# The full options card
card = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("Fitting Options", className="card-title"),
                modelDropdown,
                showConfButton,
                dbc.Collapse(confidence_Input, id=ids.CONF_COLLAPSE,is_open=False),
             
                
                extrap_Input
                
                ,
        
            ]
        ),
    ],
    style={"width": "100%"},
)




def render(app: Dash) -> html.Div:
 
    # callback to open the collapse, change button name, and plot/hide confidence bands, chained to fit button
    # Good example of a toggle button
    @app.callback(
    Output(ids.CONF_COLLAPSE, "is_open"),
    Output(ids.SHOW_CONF_BUTTON,'children'),
    Output(ids.FIT_BUTTON,'n_clicks'),
      
    Input(ids.SHOW_CONF_BUTTON, "n_clicks"),
    State(ids.CONF_COLLAPSE, "is_open"),
    State(ids.FIT_BUTTON,'n_clicks')
    )
    def toggle_collapse(n, is_open,fitn):
      
 
        if n:
            if is_open:
                name = "Show Confidence Bands"
            else:
                name = "Hide Confidence Bands"
           
            return [(not is_open), name,fitn+1]
         
                
        return [is_open,"Show Confidence Bands",fitn+1]


    return html.Div(
        [
            card
            
        ]
    )

