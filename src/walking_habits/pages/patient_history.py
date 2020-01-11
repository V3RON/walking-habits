import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output
import visdcc

from ..app import app
from ..database import traces_db, patients_db
from cloudant.query import Query
import dash_core_components as dcc
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
        selector = { 'patient': { '$eq': id }},
        # sort=[{
        #    "timestamp:number": "desc"
        # }],
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
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id="feetsensors_location_plot",
                            figure=dict(
                                data=[],
                                layout=dict(
                                    title='Feet sensors location',
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
                            ),
                            style={
                                'height': 400,
                                'width': 800,
                                'margin-top': 40,
                            }
                        )
                    ),
                    dbc.Col(
                        dcc.Graph(
                            figure=dict(
                                data=graph_data,
                                layout=dict(
                                    title='Walking trace history',
                                    showlegend=True,
                                    legend=dict(
                                        x=0,
                                        y=1.0
                                    ),
                                    margin=dict(l=40, r=0, t=40, b=100)
                                )
                            ),
                            style={
                                'height': 600,
                                'width': 1000,
                                'margin-top': 40,
                            }
                        )
                    ),
                    dcc.Graph(
                        id='basic-interactions',
                        figure=dict(
                            data=histagram_data,
                            layout=dict(
                                title='Sensors values histogram',
                                #barmode='overlay'
                            )
                        )
                    ),
                ]
            ),

        ]
    )


def get_timestamp(e):
    return float(e['timestamp'])
