from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.exceptions import PreventUpdate
import pandas as pd
import base64

from app import app

layout = html.Div(
    [
        html.Hr(),
        dbc.Row(
            [
                dbc.Card(
                    [
                        dbc.CardImg(src = '/assets/IE 172 StudyBuddy Logos.png', style = {'height' : '18%', 'width':'18%'}, top = True, className = 'align-self-center'),
                        dbc.CardHeader(
                            [
                                html.H3("StudyBuddy Database", style={'fontWeight': 'bold'}),
                            ],
                            className = 'text-center'
                        ),
                        dbc.CardBody(
                            [
                                html.H6("Online Knowledge Management System"),
                                html.P("Navigate or search through StudyBuddy's tutors, subjects, and equipment."),
                                html.Hr(),
                                html.P("For inquiries, contact us at dbsupport@studybuddy.com or reach out to your Department Manager.", style={'font-style': 'italic'}, className = 'text-light')
                            ],
                            className = 'text-center'
                        ),
                        #dbc.CardFooter(
                            #[html.P("For inquiries, contact us at dbsupport@studybuddy.com or reach out to your Departmentt Manager.", style={'font-style': 'italic'}, className = 'text-light')]
                        #),
                    ],
                    style = {
                            'width': '50%',
                            'margin': 'auto',
                            },
                    className = 'card text-white bg-info mb-3 bg-opacity-50'
                ),
                
                dbc.Carousel(
                    items=[
                        {
                            "key": "1",
                            "src": "/assets/a2.jpg",
                            "header": "Employees",
                            "caption": "Discover the right tutor from StudyBuddy's roster of exceptional employees.",
                            "img_style": {"height":"100%"}
                        },
                        {
                            "key": "2",
                            "src": "/assets/b2.jpg",
                            "header": "Expertise",
                            "caption": "Browse through the various subjects and courses that StudyBuddy offers.",
                            "img_style": {"height":"100%"}
                        },
                        {
                            "key": "3",
                            "src": "/assets/c2.jpg",
                            "header": "Equipment",
                            "caption": "Make learning easier by equipping tutors with the tools they need.",
                            "img_style": {"height":"100%"}
                        },
                    ],
                    controls=False,
                    indicators=False,
                    interval=2000,
                    style = {
                            'width': '700px',
                            'height': '300px',
                    }
                )

            ],

        )
    ],
    style = {
    'background-image': 'url(https://cms-tc.pbskids.org/parents/articles/When-to-Get-a-Math-Tutor-for-Your-Child.jpg)',
    'background-size': 'cover',
    'background-repeat': 'no-repeat',
    'background-position': 'center',
    'height': '100%',
    'left':'0px',
    'position': 'absolute',
    'vertical-align': 'top',
    'width': '100%'},
)