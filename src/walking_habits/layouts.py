from flask import current_app as server
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from .components import make_header, make_sidebar


def main_layout_header():
    return html.Div(
        [
            make_header(),
            dbc.Container(
                dbc.Row(dbc.Col(id=server.config["CONTENT_CONTAINER_ID"])), fluid=True
            ),
            dcc.Location(
                id=server.config["LOCATION_COMPONENT_ID"], refresh=False),
        ]
    )