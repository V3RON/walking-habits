from collections import Counter
from textwrap import dedent

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import CantHaveMultipleOutputs

from ..app import app
from ..database import patients_db


def fa(className):
    """A convenience component for adding Font Awesome icons"""
    return html.I(className=className)


def get_layout(**kwargs):
    return html.Div(
        [
            html.H1(className='page-title', children='Patients'),
            dbc.Row(
                get_patient_list()
            )
        ]
    )


def get_patient_list():
    cards = []
    for doc in patients_db:
        name = '{} {}'.format(doc['firstname'], doc['lastname'])
        card = dbc.Card(className='disabled' if doc['disabled'] == True else None,
                     children=[
                dbc.CardBody(
                    [
                        html.Div(className='card-corner'),
                        html.Img(className='card-image',
                                 src='assets/avatar.jpg'),
                        html.H4(name, className="card-title"),
                        html.P(children=[
                            fa("fas fa-birthday-cake"), doc['birthdate']], className="card-text"),
                    ]
                ),
                html.Div(className='card-footer', children=[
                    dbc.Button("Live", className='card-button', href='/live?id={}'.format(doc['_id']),
                                   color="primary"),
                    dbc.Button("History", className='card-button', href='/history?id={}'.format(doc['_id']),
                               color="primary"),
                ])
            ]
        )
        cards.append(dbc.Col(card, sm=12, md=4, lg=3))
    return cards
