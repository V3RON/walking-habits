from pusher import Pusher
import json, time, plotly, plotly.graph_objs as go
from datetime import datetime

pusher = Pusher(
  app_id='926549',
  key='36b976d3f19999a77a6c',
  secret='f8bf29198720e900f855',
  cluster='eu',
  ssl=True
)

SENSORS_NAMES = ["Sensor L1","Sensor L2","Sensor L3","Sensor R1","Sensor R2","Sensor R3"]

def push_data(data, id):
    times = [datetime.utcfromtimestamp(data['timestamp']).strftime('%H:%M:%S')]
    #TODO: Anomaly
    graph_data = [go.Scatter(
        x=times,
        y=[data['sensors'][sensor_id]['value']],
        name=SENSORS_NAMES[sensor_id]
        ) for sensor_id in range(0,6)]

    data_to_push = {
        'graph': json.dumps(list(graph_data), cls=plotly.utils.PlotlyJSONEncoder),
        'l1': data['sensors'][0]['value'],
        'l2': data['sensors'][1]['value'],
        'l3': data['sensors'][2]['value'],
        'r1': data['sensors'][3]['value'],
        'r2': data['sensors'][4]['value'],
        'r3': data['sensors'][5]['value'],
    }
    # trigger event
    pusher.trigger("patient_{}".format(id), "data-updated", data_to_push)
