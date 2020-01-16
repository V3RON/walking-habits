import os

from . import create_flask, create_dash
from .layouts import main_layout_header


server = create_flask()
app = create_dash(server)

with server.app_context():
    from . import index
    from . import schedule

    app.layout = main_layout_header()

    #if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    schedule.schedule_init()
