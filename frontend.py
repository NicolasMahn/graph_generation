
import dash
from dash import html, dcc, Input, Output, State, no_update, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from project import Project

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Graph Generator</title>
        <link rel="stylesheet" href="/assets/custom.css">
        {%metas%}
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            <p class="impressum">
                <b>Impressum:</b>
                Nicolas Mahn; Untere Brandstraße 62 70567 Stuttgart, Deutschland;
                Telefon: +49 (0) 152 06501315; E-Mail: nicolas.mahn@gmx.de
            </p>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Add this new Div to the layout
app.layout = dbc.Container([
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
                html.Button("Reset", id="reset-button", n_clicks=0),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div(['Drag and Drop or ', html.A('Select a File')]),
                    multiple=False
                ),
                html.Div(id="uploaded-files"),
            ])
        ], width=4),
        dbc.Col([
            html.Div(id="dashboard")
        ], width=8)
    ]),
    dcc.Interval(id="dashboard-interval", interval=2000, n_intervals=0),
    dcc.Interval(id="chat-interval", interval=1000, n_intervals=0)
], fluid=True)

# Callback to update the uploaded files display
@app.callback(
    Output("uploaded-files", "children"),
    Input("upload-data", "contents"),
    prevent_initial_call=True
)
def update_uploaded_files(upload_contents):
    files = backend.get_uploaded_files()
    return [html.Div(file) for file in files]

# Callback to update the chat history
@app.callback(
    Output("chat-history", "children"),
    Input("chat-interval", "n_intervals")
)
def update_chat_history(n_intervals):
    messages = backend.get_chat_history()
    return [html.Div(f"{msg['sender']}: {msg['text']}") for msg in messages]


# Callback to handle chat interactions and resetting.
@app.callback(
    [Input("send-chat-button", "n_clicks"),
     Input("upload-data", "contents"),
     Input("reset-button", "n_clicks")],
    [State("chat-input", "value"),
     State('upload-data', 'filename')],
    prevent_initial_call=True
)
def handle_interactions(send_chat_clicks, upload_contents, reset_clicks, chat_input, filename):
    triggered = callback_context.triggered[0]['prop_id']

    if triggered.startswith("reset-button"):
        # Reset global variables.
        backend.delete()

    elif triggered.startswith("send-chat-button"):
        if chat_input:
            backend.add_message("You", chat_input)
            # Also send the chat input through the WebSocket.

    elif triggered.startswith("upload-data"):
        backend.upload_file(upload_contents, filename)



@app.callback(
    Output("dashboard", "children"),
    Input("dashboard-interval", "n_intervals")
)
def update_dashboard_div(n_intervals):
    if (backend.get_dashboard_payload() is not None
            and isinstance(backend.get_dashboard_payload(), dict) and "code" in backend.get_dashboard_payload()):
        code_str = backend.get_dashboard_payload()["code"]
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


if __name__ == "__main__":
    try:
        backend = Project()
        # Start the Dash app.
        app.run_server(debug=True, use_reloader=False)
    except OSError as e:
        print(f"An error occurred: {e}")
