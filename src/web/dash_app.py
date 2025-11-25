# dash_app.py
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, no_update
import dash_bootstrap_components as dbc
from api.endpoints import endpoints



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
    dcc.Store(id='logged-user', storage_type='session'),
    dcc.Location(id="url-redirect", refresh='callback-nav'),
    
    dash.page_container
], className="main-container")



@app.callback(
    Output("url-redirect", "href"),
    Input("url-redirect", "pathname"),
    State("logged-user", "data")
)
def redirect_to_login(pathname, logged_user):
    # Redirect to /login as soon any page loads

    restricted_pages = ["/dashboard"]
    
    if pathname in restricted_pages and not logged_user:
        return "/login"
    
    elif pathname == "/":
        return "/login"
    
    else:    
        return no_update

if __name__ == "__main__": 
    app.run(host="0.0.0.0", port=8050, debug=True)
