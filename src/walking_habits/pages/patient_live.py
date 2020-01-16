import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output
import visdcc

from ..app import app
from ..database import patients_db
from .plots_values import xaxis, yaxis, data_scheme, shapes


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
            dbc.Card(
                dbc.CardBody([
                    html.Div(className='card-corner'),
                    html.H2(name),
                    dbc.ButtonGroup([
                        dbc.Button(
                            "History", href='/history?id={}'.format(doc['_id'])),
                        dbc.Button("Online", className='active'),
                    ])
                ]), className='page-card-header disabled' if doc['disabled'] == True else 'page-card-header',
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(className='card', children=[
                        html.Div(className='card-bg-title',
                                 children='Sensors trace graph'),
                        dcc.Graph(
                            id="trace_chart",
                            figure=dict(
                                data=data_scheme,
                                layout=dict(
                                    showlegend=True,
                                    legend=dict(x=0, y=1.0),
                                ),
                            )
                        )
                    ])
                )
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(className='card', children=[
                            html.Div(className='card-bg-title',
                                     children='Feet sensors'),
                            dcc.Graph(
                                id="feet_plot",
                                className='feet_plot_live',
                                figure=dict(
                                    data=[],
                                    layout=dict(
                                        title='Waiting for data incoming from device ...',
                                        xaxis=xaxis,
                                        yaxis=yaxis,
                                        images=[dict(
                                            source="https://i.ibb.co/B42H62v/faa2800fca9a21ede757616d49a94fa9-right-foot-hollow-clip-art-at-clkercom-vector-clip-art-online-800-600.png",
                                            xref="x",
                                            yref="y",
                                            x=0,
                                            y=5,
                                            sizex=20,
                                            sizey=20,
                                            sizing="stretch",
                                            opacity=1.0,
                                            layer="below"
                                        )],
                                        shapes=shapes,
                                    )
                                )
                            )
                        ])
                    )
                ]
            ),

            # Patient name for JS
            html.P('patient_{}'.format(id),
                   id="patient_name",
                   style={'display': 'none'}
                   )
        ]
    )
