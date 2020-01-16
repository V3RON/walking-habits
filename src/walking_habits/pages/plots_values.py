import copy

sensor_shape = dict(
    type='circle',
    xref='x',
    yref='y',
    fillcolor='rgba(255, 255, 255, 1)',
    x0=0,
    y0=0,
    x1=0,
    y1=0,
    line=dict(
        color='rgba(255, 0, 0, 1)'
    )
)

sensor_annotation = dict(
    x=0,
    y=0,
    xref='x',
    yref='y',
    text='',
    showarrow=False,
    font=dict(
        family='Courier New, monospace',
        size=25,
        color='rgba(0, 0, 0, 1)'
    )
)

sensor_data = dict(
    x=[],
    y=[],
    name='',
)

sensor_anomaly_data = dict(
    x=[],
    y=[],
    name='',
    mode='markers',
    marker=dict(
        color='blue',
        size=12
    )
)

histogram_data = dict(
    x=[],
    xbins=dict(
        start=0,
        end=1024,
        size=64
    ),
    name='',
    type='histogram'
)


def create_sensor_shape(x0, y0, x1, y1):
    s_shape = copy.deepcopy(sensor_shape)
    s_shape['x0'] = x0
    s_shape['y0'] = y0
    s_shape['x1'] = x1
    s_shape['y1'] = y1
    return s_shape


def create_sensor_annotation(x, y, text):
    s_annotation = copy.deepcopy(sensor_annotation)
    s_annotation['x'] = x
    s_annotation['y'] = y
    s_annotation['text'] = text
    return s_annotation


def create_sensor_data(name):
    s_data = copy.deepcopy(sensor_data)
    s_data['name'] = name
    return s_data


def create_sensor_anomaly_data(name, color):
    s_data = copy.deepcopy(sensor_anomaly_data)
    s_data['name'] = name
    s_data['marker']['color'] = color
    return s_data

def create_histogram_data(name):
    h_data = copy.deepcopy(histogram_data)
    h_data['name'] = name
    return h_data


shapes = [
    create_sensor_shape(4.5, 0, 6.5, -3),
    create_sensor_shape(2.5, -9, 4.5, -12),
    create_sensor_shape(1, -3, 3, -6),
    create_sensor_shape(13.5, 0, 15.5, -3),
    create_sensor_shape(15.5, -9, 17.5, -12),
    create_sensor_shape(17, -3, 19, -6),
]

annotations = [
    create_sensor_annotation(5.5, -1.5, 'L1'),
    create_sensor_annotation(3.5, -10.5, 'L3'),
    create_sensor_annotation(2, -4.5, 'L2'),
    create_sensor_annotation(14.5, -1.5, 'R1'),
    create_sensor_annotation(16.5, -10.5, 'R3'),
    create_sensor_annotation(18, -4.5, 'R2'),
]

data_scheme = [
    create_sensor_data('Sensor L1'),
    create_sensor_data('Sensor L2'),
    create_sensor_data('Sensor L3'),
    create_sensor_data('Sensor R1'),
    create_sensor_data('Sensor R2'),
    create_sensor_data('Sensor R3'),
    create_sensor_anomaly_data('L1 - Detected anomalies', 'blue'),
    create_sensor_anomaly_data('L2 - Detected anomalies', 'orange'),
    create_sensor_anomaly_data('L3 - Detected anomalies', 'green'),
    create_sensor_anomaly_data('R1 - Detected anomalies', 'red'),
    create_sensor_anomaly_data('R2 - Detected anomalies', 'purple'),
    create_sensor_anomaly_data('R3 - Detected anomalies', 'brown'),
]


histogram_scheme = [
    create_histogram_data('Sensor L1'),
    create_histogram_data('Sensor L2'),
    create_histogram_data('Sensor L3'),
    create_histogram_data('Sensor R1'),
    create_histogram_data('Sensor R2'),
    create_histogram_data('Sensor R3'),
]

xaxis = dict(
    showgrid=False,
    showline=False,
    zeroline=False,
    showticklabels=False,
    fixedrange=True,
    range=[0, 20]
)

yaxis = dict(
    showgrid=False,
    showline=False,
    zeroline=False,
    showticklabels=False,
    fixedrange=True,
    range=[-15, 5]
)
