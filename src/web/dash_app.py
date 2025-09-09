# dash_app.py
import dash
from dash.dependencies import Input, Output
from dash import dcc, html, dash_table, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import sqlite3
import pandas as pd
from flask import Flask
from api.endpoints import endpoints, get_stored_data


app = dash.Dash(__name__, url_base_pathname='/')
app.title = "Coleira Inteligente Dashboard"

app.server.register_blueprint(endpoints)

# Layout do Dash
app.layout = html.Div([
    dcc.Interval(id="interval-update", interval=500, n_intervals=0),

    html.H1("Dashboard Coleira Inteligente - TCC UNIFACCAMP", className="dashboard-title"),

    html.Div([
        dbc.Card([
            dbc.CardBody([
                html.H3("Ultima Localização conhecida", className="card-title"),
                dcc.Graph(id="loc-map", className="location-map"),
            ])
        ], className="location-card"),

        dbc.Card([
            dbc.CardBody([
                html.H3("Dados Adicionais", className="card-title"),
                html.Div(id="additional-data", className="additional-data-card")
            ])
        ], className="additional-data-section"),
    ], className="dashboard-content"),
], className="main-container")


# Callback para atualizar dados
@app.callback(
    Output("loc-map", "figure"),
    Output("additional-data", "children"),
    Input("interval-update", "n_intervals")
)
def update_dashboard(n):
    data = get_stored_data()
    print(f"Update dashboard called {n} times")

    if data['lat'] is None or data['lon'] is None:
        print("No valid data received")
        return no_update, no_update
    
    print(f"Data received: {data}")
    df = pd.DataFrame([{
        "lat": data['lat'],
        "lon": data['lon'],
        "hover_name": f"Localização do PET:\nLat: {data['lat']}, Lon: {data['lon']}"
    }])

    fig = px.scatter_map(
        df,
        lat="lat",
        lon="lon",
        hover_name="hover_name",
        zoom=15,
        center={"lat": data['lat'], "lon": data['lon']}
    )
    fig.update_traces(
        marker=dict(
            size=10,
            symbol="veterinary",  # achei mais designs em https://labs.mapbox.com/maki-icons/
            color="red"
        )
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0},
        title="Localização Atual"
    )

    battery_level = f"{data.get('battery_level', None)} %" if data.get('battery_level', None) is not None else "Waiting Data"
    heart_rate = f"{data.get('heart_rate', None)} bpm" if data.get('heart_rate', None) is not None else "Waiting Data"
    pet_body_temperature = f"{data.get('pet_body_temperature', None)} °C" if data.get('pet_body_temperature', None) is not None else "Waiting Data"
    
    additional_cards = dbc.Card([
        dbc.CardBody([
            html.H4("Battery Level", className="card-title"),
            html.P(battery_level, className="card-text")
        ]),
        dbc.CardBody([
            html.H4("PET Heart Rate", className="card-title"),
            html.P(heart_rate, className="card-text")
        ]),
        dbc.CardBody([
            html.H4("PET Body Temperature", className="card-title"),
            html.P(pet_body_temperature, className="card-text")
        ]),
        
    ])

    return fig, additional_cards


if __name__ == "__main__": 
    app.run(debug=True)
