import inspect
from functools import wraps
from urllib.parse import parse_qs

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from dash.development.base_component import Component
from flask import current_app as server
from werkzeug.datastructures import MultiDict

from .pages import page_not_found
from .exceptions import InvalidLayoutError


def component(func):
    """Decorator to help vanilla functions as pseudo Dash Components"""

    @wraps(func)
    def function_wrapper(*args, **kwargs):
        # remove className and style args from input kwargs so the component
        # function does not have to worry about clobbering them.
        className = kwargs.pop("className", None)
        style = kwargs.pop("style", None)

        # call the component function and get the result
        result = func(*args, **kwargs)

        # now restore the initial classes and styles by adding them
        # to any values the component introduced

        if className is not None:
            if hasattr(result, "className"):
                result.className = f"{className} {result.className}"
            else:
                result.className = className

        if style is not None:
            if hasattr(result, "style"):
                result.style = style.update(result.style)
            else:
                result.style = style

        return result

    return function_wrapper


class DashRouter:
    def __init__(self, app, urls):
        self.routes = {get_url(route): layout for route, layout in urls}

        @app.callback(
            Output(app.server.config["CONTENT_CONTAINER_ID"], "children"),
            [
                Input(server.config["LOCATION_COMPONENT_ID"], "pathname"),
                Input(server.config["LOCATION_COMPONENT_ID"], "search"),
            ],
        )
        def router_callback(pathname, search):
            if pathname is None:
                raise PreventUpdate("Ignoring first Location.pathname callback")

            page = self.routes.get(pathname, None)

            if page is None:
                layout = page_not_found(pathname)
            elif isinstance(page, Component):
                layout = page
            elif callable(page):
                kwargs = MultiDict(parse_qs(search.lstrip("?")))
                layout = page(**kwargs)
                if not isinstance(layout, Component):
                    msg = (
                        "Layout function must return a Dash Component.\n\n"
                        f"Function {page.__name__} from module {page.__module__} "
                        f"returned value of type {type(layout)} instead."
                    )
                    raise InvalidLayoutError(msg)
            else:
                msg = (
                    "Page layouts must be a Dash Component or a callable that "
                    f"returns a Dash Component. Received value of type {type(page)}."
                )
                raise InvalidLayoutError(msg)
            return layout

def get_dash_args_from_flask_config(config):
    """Get a dict of Dash params that were specified """
    # all arg names less 'self'
    dash_args = set(inspect.getfullargspec(dash.Dash.__init__).args[1:])
    return {key.lower(): val for key, val in config.items() if key.lower() in dash_args}


def get_url(path):
    """Expands an internal URL to include prefix the app is mounted at"""
    return f"{server.config['ROUTES_PATHNAME_PREFIX']}{path}"
