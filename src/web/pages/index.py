import dash
from dash import dcc, html, Input,State, Output, callback, no_update, ctx, clientside_callback, ClientsideFunction


dash.register_page(__name__, path='/')

layout = dash.html.Div([
    
    dash.html.H1("Welcome to the Smart Collar Dashboard"),
    dash.html.P("Please log in to access your dashboard.")
])


    