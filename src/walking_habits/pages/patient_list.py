from collections import Counter
from textwrap import dedent

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import CantHaveMultipleOutputs

from ..app import app
from ..database import patients_db


def get_layout(**kwargs):
    return html.Div(
        [
            html.H1('Patient list'),
            dbc.Row(
                get_patient_list()
            )
        ]
    )

def get_patient_list():
    cards = []
    for doc in patients_db:
        name = '{} {}'.format(doc['firstname'], doc['lastname'])
        card = html.A(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H4(name, className="card-title"),
                            html.P(
                                'Birthday: {}, disabled: {}'.format(doc['birthdate'], 'yes' if doc['disabled'] == True else 'no'),
                                className="card-text",
                            ),
                            dbc.Button("See details", className='card-button', color="primary", id='card-{}-button'.format(doc['_id'])),
                        ]
                    ),
                ]
            ), href='/details?id={}'.format(doc['_id'])
        )
        cards.append(dbc.Col(card, width=3))
    return cards