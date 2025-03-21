import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

import backend_manager

dash.register_page(__name__, path="/projects")

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H4("Select or Create a Project"),
            dcc.Input(id="project-name", type="text", placeholder="Enter project name"),
            html.Button("Create Project", id="create-project-button", n_clicks=0),
            html.Hr(),
            html.H5("Existing Projects"),
            html.Div(id="project-list")
        ])
    ]),
    dcc.Interval(id="project-interval", interval=10000000, n_intervals=0),
    dcc.Store(id="project-ids")
])

@dash.callback(
     Output("url", "pathname", allow_duplicate=True),
    [Input("create-project-button", "n_clicks")],
    [State("project-name", "value"), State("project-list", "children")],
    prevent_initial_call=True
)
def create_project(n_clicks, project_name, project_list):
    if n_clicks > 0 and project_name:
        backend_manager.create_project(project_name)
        backend_manager.project_id = project_name
        return "/dashboard"
    return dash.no_update

@dash.callback(
    [Output("project-list", "children"),
        Output("project-ids", "data")],
    Input("project-interval", "n_intervals"),
)
def update_project_list(n_intervals):
    project_ids = backend_manager.get_available_projects()

    project_list = []
    for project_id in project_ids:

        project_button = html.Button(project_id, id={'type': 'project-button', 'index': project_ids.index(project_id)}, n_clicks=0)
        project_list.append(project_button)

    return html.Div(project_list), project_ids

@dash.callback(
    Output("url", "pathname", allow_duplicate=True),
    Input({'type': 'project-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    [State({'type': 'project-button', 'index': dash.dependencies.ALL}, 'id'),
     State("project-ids", "data")],
    prevent_initial_call=True
)
def select_project(n_clicks, button_ids, project_ids):
    if any(n_clicks):
        for i, n in enumerate(n_clicks):
            if n:
                project_index = button_ids[i]['index']
                backend_manager.project_id = project_ids[project_index]
                return "/dashboard"
    return dash.no_update