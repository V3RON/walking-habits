$("head").append('<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.6/d3.min.js"></script>');


let currentChannelName = '';
let channel = null;
function myLoop() {
    setTimeout(function () {
        if (document.getElementById('trace_chart') != null && document.getElementById('feet_plot') != null) {
            if (document.getElementById('patient_name') != null &&
                currentChannelName != document.getElementById('patient_name').innerHTML) {
                if(channel == null){
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


// connect to Pusher
const feet_layout_xaxis = {
    showgrid: false,
    showline: false,
    zeroline: false,
    showticklabels: false,
    fixedrange: true,
    range: [0, 20]
};
const feet_layout_yaxis = {
    showgrid: false,
    showline: false,
    zeroline: false,
    showticklabels: false,
    fixedrange: true,
    range: [-15, 5]
};
const feet_layout_images = [
    {
        "source": "https://i.ibb.co/B42H62v/faa2800fca9a21ede757616d49a94fa9-right-foot-hollow-clip-art-at-clkercom-vector-clip-art-online-800-600.png",
        "xref": "x",
        "yref": "y",
        "x": 0,
        "y": 5,
        "sizex": 20,
        "sizey": 20,
        "sizing": "stretch",
        "opacity": 1.0,
        "layer": "below"
    },
];
const feet_layout_shapes = [
    {
        type: 'circle',
        xref: 'x',
        yref: 'y',
        fillcolor: 'rgba(255, 255, 255, 1)',
        x0: 4.5,
        y0: 0,
        x1: 6.5,
        y1: -3,
        line: {
            color: 'rgba(255, 0, 0, 1)'
        }
    },
    {
        type: 'circle',
        xref: 'x',
        yref: 'y',
        fillcolor: 'rgba(255, 255, 255, 1)',
        x0: 2.5,
        y0: -9,
        x1: 4.5,
        y1: -12,
        line: {
            color: 'rgba(255, 0, 0, 1)'
        }
    },
    {
        type: 'circle',
        xref: 'x',
        yref: 'y',
        fillcolor: 'rgba(255, 255, 255, 1)',
        x0: 1,
        y0: -3,
        x1: 3,
        y1: -6,
        line: {
            color: 'rgba(255, 0, 0, 1)'
        }
    },
    {
        type: 'circle',
        xref: 'x',
        yref: 'y',
        fillcolor: 'rgba(255, 255, 255, 1)',
        x0: 13.5,
        y0: 0,
        x1: 15.5,
        y1: -3,
        line: {
            color: 'rgba(255, 0, 0, 1)'
        }
    },
    {
        type: 'circle',
        xref: 'x',
        yref: 'y',
        fillcolor: 'rgba(255, 255, 255, 1)',
        x0: 15.5,
        y0: -9,
        x1: 17.5,
        y1: -12,
        line: {
            color: 'rgba(255, 0, 0, 1)'
        }
    },
    {
        type: 'circle',
        xref: 'x',
        yref: 'y',
        fillcolor: 'rgba(255, 255, 255, 1)',
        x0: 17,
        y0: -3,
        x1: 19,
        y1: -6,
        line: {
            color: 'rgba(255, 0, 0, 1)'
        }
    },
];
const feet_layout_annotations = [
    {
        x: 5.5,
        y: -1.5,
        xref: 'x',
        yref: 'y',
        text: 'load',
        showarrow: false,
        font: {
            family: 'Courier New, monospace',
            size: 25,
            color: 'rgba(0, 0, 0, 1)'
        }
    },
    {
        x: 3.5,
        y: -10.5,
        xref: 'x',
        yref: 'y',
        text: 'load',
        showarrow: false,
        font: {
            family: 'Courier New, monospace',
            size: 25,
            color: 'rgba(0, 0, 0, 1)'
        }
    },
    {
        x: 2,
        y: -4.5,
        xref: 'x',
        yref: 'y',
        text: 'load',
        showarrow: false,
        font: {
            family: 'Courier New, monospace',
            size: 25,
            color: 'rgba(0, 0, 0, 1)'
        }
    },
    {
        x: 14.5,
        y: -1.5,
        xref: 'x',
        yref: 'y',
        text: 'load',
        showarrow: false,
        font: {
            family: 'Courier New, monospace',
            size: 25,
            color: 'rgba(0, 0, 0, 1)'
        }
    },
    {
        x: 16.5,
        y: -10.5,
        xref: 'x',
        yref: 'y',
        text: 'load',
        showarrow: false,
        font: {
            family: 'Courier New, monospace',
            size: 25,
            color: 'rgba(0, 0, 0, 1)'
        }
    },
    {
        x: 18,
        y: -4.5,
        xref: 'x',
        yref: 'y',
        text: 'load',
        showarrow: false,
        font: {
            family: 'Courier New, monospace',
            size: 25,
            color: 'rgba(0, 0, 0, 1)'
        }
    }
];
const pusher = new Pusher('36b976d3f19999a77a6c', {
    cluster: 'eu',
    encrypted: true
});


function run() {
    Plotly.newPlot('feet_plot', [{
        x: [],
        y: []
    }], {
        'xaxis': feet_layout_xaxis,
        'yaxis': feet_layout_yaxis,
        'images': feet_layout_images,
        'shapes': feet_layout_shapes,
        'annotations': feet_layout_annotations
    }, { responsive: true }, { staticPlot: true })



    // listen for relevant events


    const initData = [{ "name": "Sensor L1", "x": [], "y": [], "type": "scatter" }, { "name": "Sensor L2", "x": [], "y": [], "type": "scatter" }, { "name": "Sensor L3", "x": [], "y": [], "type": "scatter" }, { "name": "Sensor R1", "x": [], "y": [], "type": "scatter" }, { "name": "Sensor R2", "x": [], "y": [], "type": "scatter" }, { "name": "Sensor R3", "x": [], "y": [], "type": "scatter" }];
    Plotly.newPlot('trace_chart', initData, { responsive: true }, { scrollZoom: true });

    channel.bind('data-updated', data => {
        const graph = JSON.parse(data.graph);
        const graphXY = {
            x: [graph[0].x, graph[1].x, graph[2].x, graph[3].x, graph[4].x, graph[5].x],
            y: [graph[0].y, graph[1].y, graph[2].y, graph[3].y, graph[4].y, graph[5].y]
        };
        console.log(graphXY)
        Plotly.extendTraces('trace_chart', graphXY, [0, 1, 2, 3, 4, 5])
        feet_layout_annotations[0].text = JSON.parse(data.l1);
        feet_layout_annotations[1].text = JSON.parse(data.l3);
        feet_layout_annotations[2].text = JSON.parse(data.l2);
        feet_layout_annotations[3].text = JSON.parse(data.r1);
        feet_layout_annotations[4].text = JSON.parse(data.r3);
        feet_layout_annotations[5].text = JSON.parse(data.r2);

        feet_layout_shapes[0].fillcolor = ("rgba(255,0,0," + (0.1 + JSON.parse(data.l1) / 1140) + ")");
        feet_layout_shapes[1].fillcolor = ("rgba(255,0,0," + (0.1 + JSON.parse(data.l3) / 1140) + ")");
        feet_layout_shapes[2].fillcolor = ("rgba(255,0,0," + (0.1 + JSON.parse(data.l2) / 1140) + ")");
        feet_layout_shapes[3].fillcolor = ("rgba(255,0,0," + (0.1 + JSON.parse(data.r1) / 1140) + ")");
        feet_layout_shapes[4].fillcolor = ("rgba(255,0,0," + (0.1 + JSON.parse(data.r3) / 1140) + ")");
        feet_layout_shapes[5].fillcolor = ("rgba(255,0,0," + (0.1 + JSON.parse(data.r2) / 1140) + ")");
        Plotly.update('feet_plot', [{
            x: [],
            y: []
        }], {
            'xaxis': feet_layout_xaxis,
            'yaxis': feet_layout_yaxis,
            'images': feet_layout_images,
            'shapes': feet_layout_shapes,
            'annotations': feet_layout_annotations
        })
    });
}