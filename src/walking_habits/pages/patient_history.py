import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output
import visdcc

from ..app import app
from ..database import traces_db, patients_db
from cloudant.query import Query
from datetime import datetime
from .plots_values import xaxis, yaxis, annotations, shapes, data_scheme, histogram_scheme

import copy


def get_layout(**kwargs):
    id = None

    try:
        id = kwargs['id']
    except KeyError:
        return dcc.Link('Patient not found. Click here to return to home page...', href='/')

    doc = patients_db[id]
    name = '{} {}'.format(doc['firstname'], doc['lastname'])

    query = Query(traces_db)
    resp = query(
        fields=['name', 'sensors', 'timestamp'],
        selector={'patient': {'$eq': id}},
    )

    elems = resp['docs']
    elems.sort(key=get_timestamp)
    graph_data = copy.deepcopy(data_scheme)
    histagram_data = copy.deepcopy(histogram_scheme)
    for trace in elems:
        time = datetime.utcfromtimestamp(
            trace['timestamp']).strftime('%H:%M:%S')
        for sensor in trace['sensors']:
            graph_data[sensor['id']]['y'].append(sensor['value'])
            histagram_data[sensor['id']]['x'].append(sensor['value'])
            if sensor['anomaly']:
                graph_data[sensor['id'] + 6]['x'].append(time)
                graph_data[sensor['id'] + 6]['y'].append(sensor['value'])
            graph_data[sensor['id']]['x'].append(time)

    return html.Div(
        [
            dbc.Card(
                dbc.CardBody([
                    html.Div(className='card-corner'),
                    html.H2(name),
                    dbc.ButtonGroup([
                        dbc.Button("History", className='active'),
                        dbc.Button(
                            "Online", href='/live?id={}'.format(doc['_id'])),
                    ])
                ]), className='page-card-header disabled' if doc['disabled'] == True else 'page-card-header',
            ),
            dbc.Row(
                dbc.Col(
                    html.Div(className='card', children=[
                        html.Div(className='card-bg-title',
                                 children='Walking trace history'),
                        dcc.Graph(
                            figure=dict(
                                data=graph_data,
                                layout=dict(
                                    showlegend=True,
                                    legend=dict(
                                        x=0,
                                        y=1.0
                                    ),
                                    margin=dict(l=40, r=0, t=40, b=100)
                                )
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
                                     children='Feet sensors location'),
                            dcc.Graph(
                                id="feetsensors_location_plot",
                                figure=dict(
                                    data=[],
                                    layout=dict(
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
                                        annotations=annotations
                                    )
                                )
                            )
                        ])
                    ),
                    dbc.Col(
                        html.Div(className='card', children=[
                            html.Div(className='card-bg-title',
                                     children='Sensors values histogram'),
                            dcc.Graph(
                                figure=dict(
                                    data=histagram_data,
                                )
                            )
                        ])
                    )
                ]
            ),

        ]
    )


def get_timestamp(e):
    return float(e['timestamp'])
