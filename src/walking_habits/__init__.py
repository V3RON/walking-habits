from flask import Flask
from dash import Dash

from .__version__ import __version__
from .utils import get_dash_args_from_flask_config


def create_flask(config_object=f"{__package__}.settings"):
    server = Flask(__package__)
    server.config.from_object(config_object)

    server.config.from_envvar(
        "WALKING_HABITS_SETTINGS", silent=True
    )

    return server


def create_dash(server):
    app = Dash(
        name=__package__,
        server=server,
        suppress_callback_exceptions=True,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"}
        ],
        **get_dash_args_from_flask_config(server.config)
    )

    server.config.setdefault("TITLE", "Dash")
    server.config.update({key.upper(): val for key, val in app.config.items()})

    app.title = server.config["TITLE"]

    if "SERVE_LOCALLY" in server.config:
        app.scripts.config.serve_locally = server.config["SERVE_LOCALLY"]
        app.css.config.serve_locally = server.config["SERVE_LOCALLY"]

    return app
