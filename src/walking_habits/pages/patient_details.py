import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output

from ..app import app
from ..database import patients_db

def get_layout(**kwargs):
    id = None

    try:
        id = kwargs['id']
    except KeyError:
        return dcc.Link('Patient not found. Click here to return to home page...', href='/')
        
    doc = patients_db[id]
    print(doc)
    name = '{} {}'.format(doc['firstname'], doc['lastname'])

    return html.Div(
        [
            html.Div(
                [
                    html.H1(name),
                    dbc.Badge("Disabled", color="primary", className="mr-1") if doc['disabled'] is True else None,
                    dbc.Badge(doc['birthdate'], color="primary", className="mr-1")
                ]
            ),
            dbc.Row(
                [
                    dbc.Col()
                ]
            )
        ]
    )

def get_data_card(doc):
    print(doc)
