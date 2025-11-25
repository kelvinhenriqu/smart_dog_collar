import dash
from dash import dcc, html, Input, Output, callback, no_update, ctx, clientside_callback, ClientsideFunction
import dash_bootstrap_components as dbc
import dash_qr_manager as dqm

dash.register_page(__name__, path="/login")

layout = html.Div([
    dcc.Location(id="url-redirect", refresh='callback-nav'),

    html.Div(id='qr-code-data'),
    
    html.Div([
        # Container principal centralizado
        html.Div([
            # Logo or title
            html.Div([
                html.H1("Smart Dog Collar", 
                       className="login-title",
                       style={
                           'textAlign': 'center',
                           'color': 'white',
                           'fontSize': '2.5rem',
                           'fontWeight': '700',
                           'marginBottom': '2rem',
                           'textShadow': '0 2px 4px rgba(0,0,0,0.3)'
                       })
            ]),
            
            # Card de login
            html.Div([
                html.Div([
                    dbc.Button(
                        html.I(className="bi bi-x-circle-fill", style={'fontSize': '1.2rem', 'color': '#64748b'}),
                        id="qrcode-container-close",
                        style={'position': 'absolute', 'top': '10px', 'right': '10px', 'zIndex': 2, 'background': '#00000000', 'border': 'none'}
                    ),
                    dqm.DashQrReader(
                        id='qr-code-reader',
                        videoContainerStyle={
                            'maxWidth': '400px',
                            'height': '300px',
                            'borderRadius': '12px',
                            'objectFit': 'cover',
                            'backgroundColor': '#000'
                        },
                        videoStyle={
                            'borderRadius': '12px',
                            'objectFit': 'cover'
                        }
                    ),
                    html.P("Point the camera at the QR Code", 
                               style={'textAlign': 'center', 'marginTop': '1rem', 'color': '#64748b'}),
                    
                    # Button to switch camera
                    html.Button(
                        "Switch Camera",
                        id="switch-camera-btn",
                        style={
                            'backgroundColor': '#64748b',
                            'color': 'white',
                            'border': 'none',
                            'borderRadius': '8px',
                            'padding': '8px 16px',
                            'fontSize': '0.9rem',
                            'cursor': 'pointer',
                            'marginTop': '1rem'
                        }
                    )
                ], hidden=True, id="qrcode-container", style={'position': 'relative', 'padding': '1rem', 'textAlign': 'center'}),
                        
                
                html.H3("PET Access", 
                       style={
                           'textAlign': 'center',
                           'color': '#1e293b',
                           'marginBottom': '1.5rem',
                           'fontWeight': '600'
                       }),
                
                html.P("Enter the 6-digit collar code or scan the QR Code",
                      style={
                          'textAlign': 'center',
                          'color': '#64748b',
                          'marginBottom': '2rem',
                          'fontSize': '1rem'
                      }),
                # Input do código
                html.Div([
                    dcc.Input(
                        id="pet-code-input",
                        type="text",
                        placeholder="ABC123",
                        maxLength=6,
                        style={
                            'width': '100%',
                            'height': '60px',
                            'fontSize': '1.5rem',
                            'textAlign': 'center',
                            'border': '2px solid #e2e8f0',
                            'borderRadius': '12px',
                            'padding': '0 1rem',
                            'fontWeight': '600',
                            'letterSpacing': '0.1em',
                            'textTransform': 'uppercase',
                            'outline': 'none',
                            'transition': 'all 0.3s ease'
                        }
                    )
                ], style={'marginBottom': '1.5rem'}),
                
                # Divider
                html.Div([
                    html.Hr(style={'margin': '0', 'border': '1px solid #e2e8f0', 'width': '45%'}),
                    html.Span("OR", style={
                        'padding': '0 1rem',
                        'color': '#64748b',
                        'fontSize': '0.9rem',
                        'fontWeight': '500'
                    }),
                    html.Hr(style={'margin': '0', 'border': '1px solid #e2e8f0', 'width': '45%'})
                ], style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'marginBottom': '1.5rem'
                }),
                
                # QR Code button
                html.Button([
                    html.I(className="fas fa-qrcode", style={'marginRight': '0.5rem'}),
                    "Scan QR Code"
                ], 
                id="qr-scan-btn",
                className="qr-button",
                style={
                    'width': '100%',
                    'height': '50px',
                    'backgroundColor': '#f59e0b',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '12px',
                    'fontSize': '1rem',
                    'fontWeight': '600',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s ease',
                    'marginBottom': '2rem'
                }),
                
                # Access button
                html.Button([
                    "Access Dashboard"
                ], 
                id="access-btn",
                className="access-button",
                disabled=True,
                style={
                    'width': '100%',
                    'height': '50px',
                    'backgroundColor': '#6366f1',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '12px',
                    'fontSize': '1rem',
                    'fontWeight': '600',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s ease',
                    'opacity': '0.5'
                }),
                
                # Status message
                html.Div(id="login-status", style={'marginTop': '1rem'})
                
            ], className="login-card", style={
                'backgroundColor': 'white',
                'padding': '2.5rem',
                'borderRadius': '20px',
                'boxShadow': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
                'width': '100%',
                'maxWidth': '400px'
            })
            
        ], style={
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
            'minHeight': '100vh',
            'padding': '2rem'
        })
        
    ], style={
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'minHeight': '100vh',
        'width': '100%'
    })
])

# Clientside callback to initialize camera system
clientside_callback(
    """
    function(pathname) {
        // Wait a bit to ensure the page has loaded
        setTimeout(function() {
            console.log('Initializing camera system (with delay)');
            
            // Define global variable to control camera
            if (!window.currentFacingMode) {
                window.currentFacingMode = 'environment'; // Rear camera by default
                console.log('Default camera set to rear');
            }
            
            // Intercept getUserMedia only once
            if (!window.cameraIntercepted && navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                const originalGetUserMedia = navigator.mediaDevices.getUserMedia.bind(navigator.mediaDevices);
                navigator.mediaDevices.getUserMedia = function(constraints) {
                    console.log('getUserMedia intercepted, original constraints:', constraints);
                    
                    if (constraints && constraints.video) {
                        // Apply camera configuration
                        if (typeof constraints.video === 'object') {
                            constraints.video.facingMode = { ideal: window.currentFacingMode };
                        } else {
                            constraints.video = { facingMode: { ideal: window.currentFacingMode } };
                        }
                        console.log('Using camera:', window.currentFacingMode, constraints);
                    }
                    return originalGetUserMedia(constraints);
                };
                window.cameraIntercepted = true;
                console.log('getUserMedia successfully intercepted');
            }
            
            // Define function to switch camera
            window.switchCamera = function() {
                const oldMode = window.currentFacingMode;
                window.currentFacingMode = window.currentFacingMode === 'environment' ? 'user' : 'environment';
                console.log('Switching camera from', oldMode, 'to', window.currentFacingMode);
                
                // Reload QR reader
                const qrContainer = document.getElementById('qrcode-container');
                if (qrContainer && !qrContainer.hidden) {
                    console.log('Reloading QR container');
                    qrContainer.hidden = true;
                    setTimeout(() => {
                        qrContainer.hidden = false;
                        console.log('QR container reopened with new camera');
                    }, 300);
                } else {
                    console.log('QR container not found or already hidden');
                }
            };
            
            console.log('Camera system initialized');
            console.log('window.switchCamera type:', typeof window.switchCamera);
        }, 1000); // 1 second delay
        
        return window.dash_clientside.no_update;
    }
    """,
    Output("qr-code-data", "children"),  # Dummy output
    Input("url-redirect", "pathname")
)

# Clientside callback to switch camera
clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            console.log('Switch camera button clicked:', n_clicks);
            if (typeof window.switchCamera === 'function') {
                window.switchCamera();
                console.log('switchCamera function executed');
            } else {
                console.error('switchCamera function not found');
                console.log('window.switchCamera type:', typeof window.switchCamera);
            }
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output("switch-camera-btn", "style"),  # Usar style em vez de n_clicks
    Input("switch-camera-btn", "n_clicks")
)

# Callback to validate code and enable/disable button
@callback(
    [Output("access-btn", "disabled"),
     Output("access-btn", "style"),
     Output("login-status", "children")],
    [Input("pet-code-input", "value")]
)
def validate_pet_code(code):
    if not code:
        return True, {
            'width': '100%',
            'height': '50px',
            'backgroundColor': '#6366f1',
            'color': 'white',
            'border': 'none',
            'borderRadius': '12px',
            'fontSize': '1rem',
            'fontWeight': '600',
            'cursor': 'not-allowed',
            'transition': 'all 0.3s ease',
            'opacity': '0.5'
        }, ""
    
    # Validate if code has 6 alphanumeric characters
    if len(code) == 6 and code.isalnum():
        return False, {
            'width': '100%',
            'height': '50px',
            'backgroundColor': '#10b981',
            'color': 'white',
            'border': 'none',
            'borderRadius': '12px',
            'fontSize': '1rem',
            'fontWeight': '600',
            'cursor': 'pointer',
            'transition': 'all 0.3s ease',
            'opacity': '1'
        }, html.Div([
            html.I(className="fas fa-check-circle", style={'color': '#10b981', 'marginRight': '0.5rem'}),
            "Valid code!"
        ], style={'textAlign': 'center', 'color': '#10b981', 'fontSize': '0.9rem'})
    else:
        return True, {
            'width': '100%',
            'height': '50px',
            'backgroundColor': '#6366f1',
            'color': 'white',
            'border': 'none',
            'borderRadius': '12px',
            'fontSize': '1rem',
            'fontWeight': '600',
            'cursor': 'not-allowed',
            'transition': 'all 0.3s ease',
            'opacity': '0.5'
        }, html.Div([
            html.I(className="fas fa-exclamation-circle", style={'color': '#ef4444', 'marginRight': '0.5rem'}),
            "Code must have 6 alphanumeric characters"
        ], style={'textAlign': 'center', 'color': '#ef4444', 'fontSize': '0.9rem'})

# Callback for QR Code button (placeholder for now)
@callback(
    Output("qrcode-container", "hidden", allow_duplicate=True),    
    Input("qr-scan-btn", "n_clicks"),
    Input("qrcode-container-close", "n_clicks"),
    prevent_initial_call=True
)
def simulate_qr_scan(open_click, close_click):
    input = ctx.triggered_id   
    if input == "qr-scan-btn":
        return False
    return True

@callback(
    Output("url-redirect", "href"),
    Input("access-btn", "n_clicks")
)
def access_dashboard(n_clicks):
    if n_clicks:        
        return "dashboard"
    return no_update

@callback(
    Output("pet-code-input", "value"),
    Output("qrcode-container", "hidden", allow_duplicate=True), 
    Input('qr-code-reader', 'result'),
    prevent_initial_call=True
)
def code(qr_code_data):
    print(f"result = {qr_code_data}")
    if qr_code_data:
        return qr_code_data, True    
    return no_update, False