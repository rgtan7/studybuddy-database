import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        dbc.Card(
            [
                dbc.CardImg(src = '/assets/IE 172 StudyBuddy Header.png', style = {'height' : '90%', 'width':'90%'}, top = True, className = 'align-self-center'),
                dbc.CardBody(
                    [
                        dbc.Alert('Username or password is incorrect.', color="danger", id='login_alert', is_open=False),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Input(
                                        type="text", id="login_username", placeholder="Username"
                                    ),
                                    width=8,
                                ),
                            ],
                            className="mb-3",
                            align = "center",
                            justify="center"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Input(
                                        type="text", id="login_password", placeholder="Password"
                                    ),
                                    width=8,
                                ),
                            ],
                            className="mb-3",
                            align = "center",
                            justify="center"
                        ),
                        dbc.Button('LOG IN', color="light", id='login_loginbtn', outline = "primary"),
                    ],
                    className = 'text-center'
                ),
                dbc.ListGroupItem(
                    [html.A('SIGN UP', href='/signup')], className = 'text-center'
                ),
            ],
            style = {
                    'width': '25%',
                    'margin': 'auto',
                    'top': '20%'
                    },
            className = 'card text-white bg-info mb-3 bg-opacity-50 align-self-center'
        )
    ],
    style = {
    'background-image': 'url(https://cms-tc.pbskids.org/parents/articles/When-to-Get-a-Math-Tutor-for-Your-Child.jpg)',
    'background-size': 'cover',
    'background-repeat': 'no-repeat',
    'background-position': 'center',
    'height': '100%',
    'top':'0px',
    'left':'0px',
    'position': 'absolute',
    'vertical-align': 'top',
    'width': '100%'},
)


@app.callback(
    [
        Output('login_alert', 'is_open'),
        Output('currentuserid', 'data'),
    ],
    [
        Input('login_loginbtn', 'n_clicks'), 
        Input('url', 'pathname')
    ],
    [
        State('login_username', 'value'),
        State('login_password', 'value'),   
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'), 
    ]
)
def loginprocess(loginbtn, pathname, username, password,
                 sessionlogout, currentuserid):
    openalert = False
    if pathname == '/logout':
        currentuserid = -1

    else: 
        
        if loginbtn and username and password:
            
            sql = """SELECT user_id
            FROM users
            WHERE 
                user_name = %s AND
                user_password = %s AND
                NOT user_delete_ind"""
            
            # we match the encrypted input to the encrypted password in the db
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest() 
            
            values = [username, encrypt_string(password)]
            cols = ['userid']
            df = db.querydatafromdatabase(sql, values, cols)
            
            if df.shape[0]: # if query returns rows
                currentuserid = df['userid'][0]
            else:
                currentuserid = -1
                openalert = True    
        else:
            raise PreventUpdate
        

    
    return [openalert, currentuserid]


@app.callback(
    [
        Output('url', 'pathname'),
    ],
    [
        Input('currentuserid', 'modified_timestamp'),
    ],
    [
        State('currentuserid', 'data'), 
    ]
)
def routelogin(logintime, userid):
    ctx = callback_context
    if ctx.triggered:
        if userid > 0:
            url = '/home'
        else:
            url = '/'
    else:
        raise PreventUpdate
    return [url]