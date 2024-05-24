from dash import Dash, html
import dash_bootstrap_components as dbc
#from . import card_dropdown
from . import optionsCard, inputCard, plots, fitButton, resultsCard



def create_layout(app: Dash) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
  
            html.Div([dbc.Row([   ## Whole app is one row
                            # Left hand side
                            dbc.Col([
                                html.Div(optionsCard.render(app),className="app-div"),
                                html.Div(inputCard.render(app),className="app-div"),
                                ],
                                width=4

                                ),
                            # Right hand side
                            dbc.Col([
                                fitButton.render(app),
                                plots.linFigure,
                                resultsCard.render(app)

                                ],
                                width=8
                                
                                ),
                     
                            ]),
                               
            
                    ]
                ),
          
            
            ]
        )
   