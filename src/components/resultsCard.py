# -*- coding: utf-8 -*-
"""
Created on Sun May  7 08:39:35 2023
The general options (top-left card) components and primary callback of the app
@author: jim
"""

# dash imports
from dash import Dash, html, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
#from dash.dependencies import Input, Output



# project imports
from . import ids
from ..dataHandling import tableData


tableCaption = html.Div('Estimated ranges to various levels for each model, where GS, DGS, and DCS correspond to Geometric, Damped Geometric, and Damped Cylindrical Spreading, respectively. Ranges which extend beyond measurements carry significant uncertainty.')


def buildTable(metric,fits):
    
    data,columns = tableData.getDistances(metric, fits)
    
    dataTable = dash_table.DataTable(
                id=ids.RESULTS_DATA_TABLE,
                columns=(columns                        
                
                ),
                data=data,
                style_cell={'textAlign': 'center'},
                    
            
                editable=False
            ) 
    return dataTable

# builds fit results card for each fit, depending on available parameters
def genFitResultsCard(fit):
    
    if fit.label.find('Damped')==-1:
        alpha=False
    else:
        alpha=True
    
    children =[
                html.H6(f'{fit.label} Fit', className="card-title"),
                html.Div(f'SL={fit.SL:.2f} dB'),
                html.Div(f'F={fit.F:.2f}'),
                          
                    ]
    if alpha:
        children.append(html.Div(f'alpha={fit.alpha*1000.:.3f} dB/km'))
        
    if fit.Rsquared:
        children.append(html.Div(f'Rsq={fit.Rsquared:.3f} '))
    
    card = dbc.Card(
        [
    
            dbc.CardBody(children)                             
        ],
        style={"width": "100%"},
    )
    return card

# updates the full results card
def updateCard(metric,fits):
    children = [html.H4("Fit Results", className="card-title")]                           
                
    dataTable = buildTable(metric, fits)
    
    # fit results/parameters for each model column
    inCol = []
    for fit in fits:
        inCol.append(genFitResultsCard(fit))
        
    resultsRow = dbc.Row([
                    dbc.Col(inCol),
                    dbc.Col(children=[dataTable, tableCaption])      
                    ]
                )    
    children.append(resultsRow)    
    return children

# Blank initial results card
card = dbc.Card(
    [

        dbc.CardBody(
            [
                html.H4("Results", className="card-title"),

            ],
            id=ids.RESULTS_CARD
        ),
    ],
    style={"width": "100%"},
)




def render(app: Dash) -> html.Div:

    return html.Div(
        [
            card
            
        ]
    )


