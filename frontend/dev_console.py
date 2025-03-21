import dash
from dash import html, dcc, Input, Output, State, no_update, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from pygments.lexer import default

import backend_manager

dash.register_page(__name__, path="/dev_console")

# Add this new Div to the layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4("Chat"),
                dcc.Dropdown(id="dev-chat-dropdown", placeholder="select chat"),
                html.Div(id="dev-chat-history"),
                dcc.Textarea(
                    id="dev-chat-input",
                    placeholder="Enter your message..."
                ),
                html.Button("Send", id="dev-send-chat-button", n_clicks=0),
            ])
        ], width=6),
        dbc.Col([
            dcc.Dropdown(id="dev-code-version", placeholder="select a code version (default latest)", value="latest"),
            html.Div(id="dev-code")
        ], width=6)
    ]),
    dcc.Interval(id="dev-interval", interval=1000, n_intervals=0),
    html.Button("Switch View", id="dev-switch-view-button", n_clicks=0,
                style={"position": "fixed", "bottom": "10px", "left": "10px"})
], fluid=True)

@dash.callback(
    Output("dev-code-version", "options"),
    Input("dev-interval", "n_intervals")
)
def update_code_dropdown_dev(n_intervals):
    return backend_manager.get_code_names()

@dash.callback(
    Output("dev-code", "children"),
    Input("dev-code-version", "value")
)
def update_code_div_dev(version):
    code_logs_output = backend_manager.get_code(version)
    if not code_logs_output or isinstance(code_logs_output, str):
        return dcc.Markdown(f"```{code_logs_output}```")
    code = code_logs_output[0]
    logs = code_logs_output[1]
    output = code_logs_output[2]
    return html.Div([
        dcc.Markdown(f"```python {code}```"),
        dcc.Markdown(f"```log {logs}```"),
        html.Label("Output:"),
        dcc.Markdown(f"```{output}```")
    ])


@dash.callback(
    Output("dev-chat-dropdown", "options"),
    Input("dev-interval", "n_intervals")
)
def update_chat_dropdown(n_intervals):
    chats = backend_manager.get_available_chats()
    return [{"label": chat, "value": chat} for chat in chats]

# Callback to update the chat history
@dash.callback(
    Output("dev-chat-history", "children"),
    [Input("dev-interval", "n_intervals"),
     Input("dev-chat-dropdown", "value")]
)
def update_chat_history_dev(n_intervals, selected_chat):
    if selected_chat:
        messages = backend_manager.get_chat_history(selected_chat)
        return [dcc.Markdown(f"\*{msg['sender']}\*:\n{msg['text']}") for msg in messages]
    messages = backend_manager.get_chat_history("customer_chat")
    return [dcc.Markdown(f"\*{msg['sender']}\*:\n{msg['text']}") for msg in messages]

@dash.callback(
    Input("dev-send-chat-button", "n_clicks"),
    [State("dev-chat-input", "value"),
     State("dev-chat-dropdown", "value")],
    prevent_initial_call=True
)
def handle_interactions_dev(send_chat_clicks, chat_input, selected_chat):
    if send_chat_clicks > 0:
        if chat_input:
            backend_manager.add_message(selected_chat, chat_input)
    pass


@dash.callback(
    Output("url", "pathname", allow_duplicate=True),
    Input("dev-switch-view-button", "n_clicks"),
    prevent_initial_call=True
)
def handle_switch_view_dev(switch_view_clicks):
    if switch_view_clicks > 0:
        return "/dashboard"
    return dash.no_update