# -*- coding: utf-8 -*-
"""
Created on Sun May  7 08:39:35 2023
The general options (top-left card) components and primary callback of the app
@author: jim
"""

# dash imports
from dash import Dash, html, Input, Output, State
import dash_bootstrap_components as dbc
#from dash.dependencies import Input, Output

# data science imports
import pandas as pd

# project imports
from . import ids, plots, resultsCard
from ..dataHandling import TLfitting as TLF






button = html.Div(
    [   dbc.Row(
        [     
            dbc.Col(dbc.Button("Fit Data", id=ids.FIT_BUTTON, className="button", n_clicks=0)),
             
        ]
      )
    ]
        
)


### Wrapped fit methods
def linFit(df,parameters):
   
    if parameters['confBands']:
        confInt = 1-parameters['confInt']*.01
    else:
        confInt = None
        
    fit = TLF.linTLfit(df['range_m'], df['level'],
                       newr_ext=parameters['extrap'],
                       confidenceInterval=confInt)
    
    return fit

def dgFit(df,parameters):
   
    if parameters['confBands']:
        confInt = 1-parameters['confInt']*.01
    else:
        confInt = None
        
    fit = TLF.dampedTLfit(df['range_m'], df['level'],
                       newr_ext=parameters['extrap'],
                       confidenceInterval=confInt)
    
    return fit

def dcFit(df,parameters):
   
    if parameters['confBands']:
        confInt = 1-parameters['confInt']*.01
    else:
        confInt = None
        
    fit = TLF.dampedTLfit(df['range_m'], df['level'],
                       newr_ext=parameters['extrap'],
                       confidenceInterval=confInt,DCS=True)
    
    return fit

fitMethods = {'Geometric Spreading': linFit, 'Damped Geometric Spreading': dgFit, 'Damped Cylindrical Spreading': dcFit}


def render(app: Dash) -> html.Div:
 
    # main callback, does all the work
    @app.callback(
        
        output = [Output(ids.LIN_PLOT,'figure',allow_duplicate=True),
                  Output(ids.RESULTS_CARD,'children')],
        inputs = dict(nclicks=Input(ids.FIT_BUTTON, "n_clicks")),
        state = dict(parameters=
                      dict(extrap = State(ids.EXTRAP_INPUT, "value"),
                          confInt = State(ids.CONF_INT_INPUT, "value"),
                          models = State(ids.MODEL_DROPDOWN,'value'),
                          data = State(ids.DATA_TABLE,'data'),
                          confBands = State(ids.CONF_COLLAPSE,'is_open'),
                          metric = State(ids.METRIC_DROPDOWN,'value')
    
                          )
                      ),
        prevent_initial_call=True
        )
        
      
        
    def fit_callback(nclicks,parameters):
        if nclicks:
            df = pd.DataFrame(data = parameters['data'],dtype=float)
       
            fits = [fitMethods[model](df,parameters) for model in parameters['models']]
            
            resultsCardChildren = resultsCard.updateCard(parameters['metric'],fits) 
                    
            fig = plots.plotFit(df, fits,confBands=parameters['confBands'])
                    
                    
            
            return fig, resultsCardChildren
    return button
            
