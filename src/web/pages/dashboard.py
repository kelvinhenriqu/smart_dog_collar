import dash
from dash.dependencies import Input, Output
from dash import dcc, html, no_update, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from api.endpoints import endpoints, get_location_history, get_stored_data
import requests



dash.register_page(__name__, path='/dashboard')

layout  = html.Div([
    dcc.Interval(id="interval-update", interval=500, n_intervals=0),
    dcc.Tooltip(id="tooltip"),
    dcc.Store(id="fullscreen-state", data=False),
    html.Button([
        html.I(className="bi bi-x-lg", style={"marginRight": "8px"}),
        "Close Fullscreen"
    ], id="close-fullscreen-btn", className="close-fullscreen-btn", style={"display": "none"}),
    html.Div(id="fullscreen-overlay", className="fullscreen-overlay", style={"display": "none"}),
    
    dbc.Row([ #Header Row
        dbc.Col([
            html.H1([
                html.I(className="bi bi-geo-alt-fill", style={"marginRight": "15px", "color": "#fbbf24"}),
                "Dashboard Smart Collar - TCC UNIFACCAMP"
            ], className="dashboard-title"),
        ], xs=12, sm=12, md=10, lg=10, className="dashboard-header"),

        dbc.Col([
            dcc.Upload(
                id="upload-data",
                children=html.Button(className="bi bi-person",style={"fontSize": "2.5rem"},id="profile-icon-btn"),
                multiple=False,
                className="profile-icon-btn",
            )
        ], xs=12, sm=12, md=2, lg=2, className="dashboard-header"),
    ], align="center", justify="between", className="dashboard-header-row"),

    html.Div([ #Main Content
        dbc.Card([            
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([                
                        html.H3([
                            html.I(className="bi bi-map", style={"marginRight": "10px", "color": "#6366f1"}),
                            "Last known location & Tracking"
                        ], className="card-title"),                        
                    ], width=12),
                ]),
                dbc.Row([  
                    dbc.Col([
                        dcc.Dropdown(
                            id="period-dropdown",
                            options=[
                                {"label": "📍 Last 5 minutes", "value": 5},
                                {"label": "🕐 Last 30 minutes", "value": 30},
                                {"label": "⏰ Last 60 minutes", "value": 60},
                                {"label": "📅 Last day", "value": 1440},
                                {"label": "📆 Last 3 days", "value": 4320},
                            ],
                            value=60,
                            clearable=False,
                            style={
                                "width": "100%",
                                "fontWeight": "500"
                            }
                        )
                    ], style={"paddingRight": "10px", "width": "90%"}),
                    dbc.Col([
                        html.Button([
                            html.I(className="bi bi-arrows-fullscreen", style={"fontSize": "1.2rem"})
                        ], id="fullscreen-btn", className="fullscreen-btn", n_clicks=0)
                    ], style={"width": "10%","display":"contents"}),

                ], style={"marginBottom": "15px"}, class_name="history_selection_row"),
                dbc.Row([
                    dcc.Graph(
                        id="loc-map", 
                        className="location-map",
                        config={
                            'displayModeBar': False,
                            'doubleClick': 'reset+autosize'
                        }
                    ),
                ], id="map-container")
            ], className="location-card"),
        ], className="location-section"),
        dbc.Card([
            dbc.CardBody([
                html.H3([
                    html.I(className="bi bi-activity", style={"marginRight": "10px", "color": "#6366f1"}),
                    "Pet Health Monitor"
                ], className="card-title"),
                html.Div(id="additional-data", className="additional-data-card")
            ])
        ], className="additional-data-section"),
    ], className="dashboard-content"),

])


@callback(
    Output("upload-data", "children"),
    Input("upload-data", "contents"),
)
def update_profile_icon(image_content):
    if image_content is not None:
        data = html.Img(src=image_content, style={"height": "100px", "width": "100px", "borderRadius": "100px", "border": "2px solid"})
        return data
    
    return no_update

@callback(
    Output("map-container", "style"),
    Output("fullscreen-btn", "children"),
    Output("fullscreen-state", "data"),
    Output("close-fullscreen-btn", "style"),
    Output("fullscreen-overlay", "style"),
    Input("fullscreen-btn", "n_clicks"),
    Input("close-fullscreen-btn", "n_clicks"),
    Input("fullscreen-state", "data"),
    prevent_initial_call=True
)
def toggle_fullscreen(fullscreen_clicks, close_clicks, is_fullscreen):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return {}, [html.I(className="bi bi-arrows-fullscreen", style={"fontSize": "1.2rem"})], False, {"display": "none"}, {"display": "none"}
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    # Toggle state based on which button was clicked
    if button_id == "fullscreen-btn":
        new_state = not is_fullscreen
    elif button_id == "close-fullscreen-btn":
        new_state = False
    else:
        new_state = is_fullscreen
    
    if new_state:
        # Fullscreen mode
        return {
            "position": "fixed",
            "top": "0",
            "left": "0",
            "width": "100vw",
            "height": "100vh",
            "zIndex": "9999",
            "backgroundColor": "#ffffff",
            "padding": "60px 20px 20px 20px",
            "margin": "0"
        }, [html.I(className="bi bi-arrows-fullscreen", style={"fontSize": "1.2rem"})], True, {
            "display": "flex",
            "position": "fixed",
            "top": "10px",
            "right": "10px",
            "zIndex": "10000"
        }, {
            "display": "block"
        }
    else:
        # Normal mode
        return {}, [html.I(className="bi bi-arrows-fullscreen", style={"fontSize": "1.2rem"})], False, {"display": "none"}, {"display": "none"}

@callback(
    Output("loc-map", "figure"),
    Output("additional-data", "children"),
    Input("interval-update", "n_intervals"),
    Input("period-dropdown", "value")
)
def update_dashboard(n, period):

    history = get_location_history(period)

    data = get_stored_data()

    if not history:
        print("No tracking data available.")
        fig = go.Figure()
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r":0,"t":0,"l":0,"b":0},
            template="plotly_white",
            xaxis={'visible': False},
            yaxis={'visible': False},
            annotations=[
                dict(
                    text="No tracking data available.",
                    xref="paper", yref="paper",
                    showarrow=False,
                    font=dict(size=20),
                    x=0.5, y=0.5
                )
            ]
        )

    else:
        last = history[-1]
        df = pd.DataFrame(history)

        if period < 60:
            fig_title = f"🗺️ Pet tracking - Last {period} minutes"
        elif period < 1440:
            fig_title = f"🗺️ Pet tracking - Last {period // 60} hours"
        else:
            fig_title = f"🗺️ Pet tracking - Last {period // 1440} days"


        fig = px.scatter_map(
            df,
            lat="lat",
            lon="lon",
            hover_name="timestamp",
            zoom=16,
            center={"lat": last['lat'], "lon": last['lon']},
            title=fig_title,
            color_discrete_sequence=['#6366f1']
        )
        fig.add_trace(go.Scattermap(
            lat=[last['lat']],
            lon=[last['lon']],
            mode='markers',
            marker=dict(size=20, color='#f59e0b', symbol='veterinary'), #icons here: https://labs.mapbox.com/maki-icons/
            name='🐕 Current Position',
            hovertemplate='<b>Current Location</b><br>Lat: %{lat}<br>Lon: %{lon}<extra></extra>'
        ))
        fig.update_layout(
            mapbox_style="open-street-map",
            margin={"r":0,"t":40,"l":0,"b":0},
            title={
                'text': f"{fig_title}",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 18, 'family': 'Poppins, sans-serif', 'color': '#1e293b'}
            },
            font={'family': 'Inter, sans-serif'},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=0.01,
                xanchor="center",
                x=0.5,
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#e2e8f0",
                borderwidth=1,
                font=dict(size=11)
            ),
            height=600
        )


    battery_level = data.get("battery_level", "-")
    heart_rate = data.get("heart_rate", "-")
    pet_body_temperature = data.get("pet_body_temperature", "-")
    vel = data.get("velocidade", 0)
    try:
        velocidade = round(float(vel), 1)
    except (ValueError, TypeError):
        velocidade = "-"
    satelites = data.get("satelites", "-")
    status = data.get("status", "-")

    # Determine status indicators based on values
    def get_battery_status(level):
        if level == "-":
            return "status-offline"
        try:
            level_num = int(level)
            if level_num > 50:
                return "status-online"
            elif level_num > 20:
                return "status-warning"
            else:
                return "status-offline"
        except:
            return "status-offline"

    def get_heart_rate_status(hr):
        if hr == "-":
            return "status-offline"
        try:
            hr_num = int(hr)
            if 60 <= hr_num <= 120:  # Normal range for dogs
                return "status-online"
            else:
                return "status-warning"
        except:
            return "status-offline"

    def get_temperature_status(temp):
        if temp == "-":
            return "status-offline"
        try:
            temp_num = float(temp)
            if 38.0 <= temp_num <= 39.5:  # Normal range for dogs
                return "status-online"
            else:
                return "status-warning"
        except:
            return "status-offline"

    additional_cards = html.Div([
        html.Div([
            html.H5([
                html.Span(className=f"status-indicator {get_battery_status(battery_level)}"),
                "🔋 Battery Level"
            ]),
            html.P(f"{battery_level}%" if battery_level != "-" else "Offline")
        ], className="data-metric"),
        
        html.Div([
            html.H5([
                html.Span(className=f"status-indicator {get_heart_rate_status(heart_rate)}"),
                "❤️ Heart Rate"
            ]),
            html.P(f"{heart_rate} bpm" if heart_rate != "-" else "No Signal")
        ], className="data-metric"),
        
        html.Div([
            html.H5([
                html.Span(className=f"status-indicator {get_temperature_status(pet_body_temperature)}"),
                "🌡️ Body Temperature"
            ]),
            html.P(f"{pet_body_temperature} °C" if pet_body_temperature != "-" else "No Reading")
        ], className="data-metric"),
        
        html.Div([
            html.H5("🚀 Velocidade Estimada"),
            html.P(f"{velocidade} km/h" if velocidade != "-" else "No Data")
        ], className="data-metric"),
        
        html.Div([
            html.H5("🛰️ Satélites Conectados"),
            html.P(f"{satelites}" if satelites != "-" else "No Signal")
        ], className="data-metric"),
        
        html.Div([
            html.H5("📡 Connection Status"),
            html.P(f"{status}")
        ], className="data-metric"),
    ])

    return fig, additional_cards
