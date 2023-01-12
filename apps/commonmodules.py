from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from app import app
from dash import Dash
import logging

from urllib.parse import urlparse, parse_qs

navlink_style = {
    'color': '#fff'
}

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(html.Img(src = '/assets/IE 172 StudyBuddy Header.png', style = {'height' : '30%', 'width':'30%'}, height="30px")),
                ],
                align="center",
            ),
            href="/home",
        ),
        dbc.NavLink("Home", href="/home", style=navlink_style),
        dbc.NavLink("Directory", href="/directory", style=navlink_style),
        dbc.NavLink("Areas of Expertise", href="/aoe", style=navlink_style),
        dbc.NavLink("Equipment", href="/equipment", style=navlink_style),
        dbc.NavLink("Logout", href='/logout', style=navlink_style ),
        
    ],
    dark=True,
    color='info'
)   