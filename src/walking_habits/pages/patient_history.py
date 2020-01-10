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


def get_layout(**kwargs):
    id = None

    try:
        id = kwargs['id']
    except KeyError:
        return dcc.Link('Patient not found. Click here to return to home page...', href='/')

    doc = patients_db[id]
    name = '{} {}'.format(doc['firstname'], doc['lastname'])

    i = 0
    traces = [list() for y in range(6)]
    time = list()

    query = Query(traces_db)
    resp = query(
        fields=['name','sensors','timestamp'],
        selector={'$text': 'alek'}
    )

    for trace in resp['docs']:
        for sensor in trace['sensors']:
            traces[sensor['id']].append(sensor['value'])
        time.append(datetime.utcfromtimestamp(
            trace['timestamp']).strftime('%d-%m-%Y %H:%M:%S'))

    print(traces)
    return html.Div(
        [
            html.Div(
                [
                    html.H1(name),
                    dbc.Badge("Disabled", color="primary",
                              className="mr-1") if doc['disabled'] is True else None,
                ]
            ),
            dcc.Graph(
                id="feet_plot",
                figure=dict(
                    data=[
                        dict(
                            x=time,
                            y=traces[0],
                            name='Sensor L1',
                            # marker=dict(
                            #    color='rgb(55, 83, 109)'
                            # )
                        ),
                        dict(
                            x=time,
                            y=traces[1],
                            name='Sensor L2',
                            # marker=dict(
                            #    color='rgb(26, 118, 255)'
                            # )
                        ),
                        dict(
                            x=time,
                            y=traces[2],
                            name='Sensor L3',
                            # marker=dict(
                            #    color='rgb(55, 83, 109)'
                            # )
                        ),
                        dict(
                            x=time,
                            y=traces[3],
                            name='Sensor R1',
                            # marker=dict(
                            #    color='rgb(26, 118, 255)'
                            # )
                        ),
                        dict(
                            x=time,
                            y=traces[4],
                            name='Sensor R2',
                            # marker=dict(
                            #    color='rgb(55, 83, 109)'
                            # )
                        ),
                        dict(
                            x=time,
                            y=traces[5],
                            name='Sensor R3',
                            # marker=dict(
                            #    color='rgb(26, 118, 255)'
                            # )
                        )
                    ],
                    layout=dict(
                        title='Still TODO',
                        showlegend=True,
                        legend=dict(
                            x=0,
                            y=1.0
                        ),
                        margin=dict(l=40, r=0, t=40, b=30)
                    )
                ),
                #style={'height': 300},
            )

        ]
    )
