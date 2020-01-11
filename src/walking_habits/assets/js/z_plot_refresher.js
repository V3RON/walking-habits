let currentChannelName = '';
let channel = null;
function myLoop() {
    setTimeout(function () {
        if (document.getElementById('trace_chart') != null && document.getElementById('feet_plot') != null) {
            if (document.getElementById('patient_name') != null &&
                currentChannelName != document.getElementById('patient_name').innerHTML) {
                if (channel == null) {
                    pusher.unsubscribe(currentChannelName);
                }
                currentChannelName = document.getElementById('patient_name').innerHTML;
                channel = pusher.subscribe(currentChannelName);
                run();
            }
        } else {
            pusher.unsubscribe(currentChannelName);
            currentChannelName = '';
        }
        myLoop();
    }, 1000)
}

myLoop();

const sensor_shape = {
    type: 'circle',
    xref: 'x',
    yref: 'y',
    fillcolor: 'rgba(255, 255, 255, 1)',
    x0: 0,
    y0: 0,
    x1: 0,
    y1: 0,
    line: {
        color: 'rgba(255, 0, 0, 1)'
    }
}

const sensor_annotation = {
    x: 0,
    y: 0,
    xref: 'x',
    yref: 'y',
    text: '',
    showarrow: false,
    font: {
        family: 'Courier New, monospace',
        size: 14,
        color: 'rgba(0, 0, 0, 1)'
    }
}

function create_sensor_shape(x0, y0, x1, y1) {
    let s_shape = { ...sensor_shape };
    s_shape.x0 = x0;
    s_shape.y0 = y0;
    s_shape.x1 = x1;
    s_shape.y1 = y1;
    return s_shape;
}

function create_sensor_annotation(x,y,text){
    let s_annotation = { ...sensor_annotation };
    s_annotation.x = x;
    s_annotation.y = y;
    s_annotation.text = text;
    return s_annotation;
}

const feet_layout_shapes = [
    create_sensor_shape(4.5, 0, 6.5, -3),
    create_sensor_shape(2.5, -9, 4.5, -12),
    create_sensor_shape(1, -3, 3, -6),
    create_sensor_shape(13.5, 0, 15.5, -3),
    create_sensor_shape(15.5, -9, 17.5, -12),
    create_sensor_shape(17, -3, 19, -6),
];
const feet_layout_annotations = [
    create_sensor_annotation(5.5, -1.5, 'L1'),
    create_sensor_annotation(3.5, -10.5, 'L3'),
    create_sensor_annotation(2, -4.5, 'L2'),
    create_sensor_annotation(14.5, -1.5, 'R1'),
    create_sensor_annotation(16.5, -10.5, 'R3'),
    create_sensor_annotation(18, -4.5, 'R2'),
];
const pusher = new Pusher('36b976d3f19999a77a6c', {
    cluster: 'eu',
    encrypted: true
});


function run() {
    channel.bind('data-updated', data => {
        Plotly.extendTraces('trace_chart', data.graph, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        
        feet_layout_annotations[0].text = 'L1:' + data.graph['y'][0];
        feet_layout_annotations[1].text = 'L3:' + data.graph['y'][1];
        feet_layout_annotations[2].text = 'L2:' + data.graph['y'][2];
        feet_layout_annotations[3].text = 'R1:' + data.graph['y'][3];
        feet_layout_annotations[4].text = 'R3:' + data.graph['y'][4];
        feet_layout_annotations[5].text = 'R2:' + data.graph['y'][5];

        feet_layout_shapes[0].fillcolor = ("rgba(255,0,0," + (0.1 + data.graph['y'][0] / 1140) + ")");
        feet_layout_shapes[1].fillcolor = ("rgba(255,0,0," + (0.1 + data.graph['y'][1] / 1140) + ")");
        feet_layout_shapes[2].fillcolor = ("rgba(255,0,0," + (0.1 + data.graph['y'][2] / 1140) + ")");
        feet_layout_shapes[3].fillcolor = ("rgba(255,0,0," + (0.1 + data.graph['y'][3] / 1140) + ")");
        feet_layout_shapes[4].fillcolor = ("rgba(255,0,0," + (0.1 + data.graph['y'][4] / 1140) + ")");
        feet_layout_shapes[5].fillcolor = ("rgba(255,0,0," + (0.1 + data.graph['y'][5] / 1140) + ")");
        Plotly.update('feet_plot', [], {
            'title': "",
            'shapes': feet_layout_shapes,
            'annotations': feet_layout_annotations
        })
    });
}