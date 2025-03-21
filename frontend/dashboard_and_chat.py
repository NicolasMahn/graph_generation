
import dash
from dash import html, dcc, Input, Output, State, no_update, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from pygments.lexer import default

import backend_manager

dash.register_page(__name__, path="/dashboard")

# Add this new Div to the layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4("Chat"),
                html.Div(id="chat-history"),
                dcc.Textarea(
                    id="chat-input",
                    placeholder="Enter your message..."
                ),
                html.Button("Send", id="send-chat-button", n_clicks=0),
                html.Button("Delete Project", id="reset-button", n_clicks=0),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div(['Drag and Drop or ', html.A('Select a File')]),
                    multiple=False
                ),
                html.Div(id="uploaded-files"),
            ])
        ], width=8),
        dbc.Col([
            html.Div(id="dashboard")
        ], width=4)
    ]),
    dcc.Interval(id="dashboard-interval", interval=10000, n_intervals=0),
    dcc.Interval(id="chat-interval", interval=1000, n_intervals=0),
    html.Button("Switch View", id="switch-view-button", n_clicks=0,
                style={"position": "fixed", "bottom": "10px", "left": "10px"})
], fluid=True)

# Callback to update the uploaded files display
@dash.callback(
    Output("uploaded-files", "children"),
    Input("upload-data", "contents"),
    prevent_initial_call=True
)
def update_uploaded_files(upload_contents):
    files = backend_manager.get_uploaded_files()
    return [html.Div(file) for file in files]

# Callback to update the chat history
@dash.callback(
    Output("chat-history", "children"),
    Input("chat-interval", "n_intervals")
)
def update_chat_history(n_intervals):

    messages = backend_manager.get_chat_history("customer_chat")
    return [dcc.Markdown(f"\*{msg['sender']}\*:\n{msg['text']}") for msg in messages]


# Callback to handle chat interactions and resetting.
@dash.callback(
Output("url", "pathname", allow_duplicate=True),
    [Input("send-chat-button", "n_clicks"),
     Input("upload-data", "contents"),
     Input("reset-button", "n_clicks"),
     Input("switch-view-button", "n_clicks")],
    [State("chat-input", "value"),
     State('upload-data', 'filename')],
    prevent_initial_call=True
)
def handle_interactions(send_chat_clicks, upload_contents, reset_clicks, switch_view_clicks, chat_input, filename):
    triggered = callback_context.triggered[0]['prop_id']

    if triggered.startswith("reset-button"):
        # Reset global variables.
        backend_manager.delete_project()
        return "/projects"

    elif triggered.startswith("send-chat-button"):
        if chat_input:
            backend_manager.add_message("customer_chat", chat_input)
            # Also send the chat input through the WebSocket.

    elif triggered.startswith("upload-data"):
        backend_manager.upload_file(upload_contents, filename)


    elif triggered.startswith("switch-view-button"):
        return "/dev_console"

    return dash.no_update


@dash.callback(
    Output("dashboard", "children"),
    Input("dashboard-interval", "n_intervals")
)
def update_dashboard_div(n_intervals):
    dashboard_payload = backend_manager.get_dashboard_payload()
    if (dashboard_payload is not None
            and isinstance(dashboard_payload, dict) and "code" in dashboard_payload):
        code_str = dashboard_payload["code"]
        # Create a restricted globals dictionary (only allowing safe objects)
        allowed_globals = {"html": html, "dcc": dcc, "go": go}
        allowed_locals = {}
        try:
            # Execute the provided code and store the result in 'result'
            exec("result = " + code_str, allowed_globals, allowed_locals)
            return allowed_locals.get("result", html.Div("No result"))
        except Exception as e:
            return html.Div(f"Error executing code: {str(e)}")
    return None