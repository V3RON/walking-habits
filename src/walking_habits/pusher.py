from pusher import Pusher
import json
import time
import plotly
import plotly.graph_objs as go
from datetime import datetime

pusher = Pusher(
    app_id='926549',
    key='36b976d3f19999a77a6c',
    secret='f8bf29198720e900f855',
    cluster='eu',
    ssl=True
)


def push_data(data, id):
    data_time = [datetime.utcfromtimestamp(
        data['timestamp']).strftime('%H:%M:%S')]

    graph_data = dict(
        x= [],
        y= []
    )

    for sensor_id in range(0, 6):
        graph_data['x'].append(data_time)
        graph_data['y'].append([data['sensors'][sensor_id]['value']])

    for sensor_id in range(0, 6):
        if data['sensors'][sensor_id]['anomaly']:
            graph_data['x'].append(data_time)
            graph_data['y'].append([data['sensors'][sensor_id]['value']])
        else:
            graph_data['x'].append([])
            graph_data['y'].append([])

    data_to_push = {
        'graph': graph_data,
    }
    # trigger event
    pusher.trigger("patient_{}".format(id), "data-updated", data_to_push)
