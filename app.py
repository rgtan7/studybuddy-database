import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import logging
from dash import Dash

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

app.config.suppress_callback_exceptions = True

app.css.config.serve_locally = True

app.scripts.config.serve_locally = True

app.title = 'StudyBuddy'

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)