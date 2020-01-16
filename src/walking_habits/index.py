import dash_html_components as html

from .app import app
from .utils import DashRouter
from .pages import patient_list, patient_live, patient_history


urls = (
    ("", patient_list.get_layout),
    ("list", patient_list.get_layout),
    ("live", patient_live.get_layout),
    ("history", patient_history.get_layout)
)

router = DashRouter(app, urls)
