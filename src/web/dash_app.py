# dash_app.py
import dash
from dash.dependencies import Input, Output
from dash import dcc, html, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from api.endpoints import endpoints, get_location_history, get_stored_data
import requests



external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css"
]

external_scripts = [
    "https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.min.js"
]

app = dash.Dash(__name__, 
                url_base_pathname='/', 
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                use_pages=True)
app.title = "smart-collar-dashboard"

server = app.server
server.register_blueprint(endpoints)

# Layout do Dash
app.layout = html.Div([
    dash.page_container
], className="main-container")



if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=8050, debug=True)
