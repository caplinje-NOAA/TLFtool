
from dash import Dash
from dash_bootstrap_components.themes import CERULEAN


from src.components.layout import create_layout



app = Dash(external_stylesheets=[CERULEAN],prevent_initial_callbacks=True)
app.title = "OPR-A TL Fitting Tool"
app.layout = create_layout(app)
app.config.suppress_callback_exceptions = True



if __name__ == "__main__":
    app.run(debug=True)


# DASH LEAFLET IS THE WAY