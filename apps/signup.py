import hashlib

import dash_bootstrap_components as dbc
from dash import dcc, html
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
                        html.H2('Enter Account details'),
                        html.Hr(),
                        dbc.Alert('Please supply details.', color="danger", id='signup_alert',
                                  is_open=False),
                        dbc.Row(
                            [
                                dbc.Label("Username", width=5),
                                dbc.Col(
                                    dbc.Input(
                                        type="text", id="signup_username", placeholder="Enter a username"
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Password", width=5),
                                dbc.Col(
                                    dbc.Input(
                                        type="password", id="signup_password", placeholder="Enter a password"
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Label(" Confirm Password", width=5),
                                dbc.Col(
                                    dbc.Input(
                                        type="password", id="signup_passwordconf", placeholder="Re-type the password"
                                    ),
                                    width=6,
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Button('Sign up', color="light", outline="primary", id='singup_signupbtn', className = {'textAlign' :'center', 'verticalAlign' : 'middle'}),
                    ],
                ),
            ],
            style = {
                    'width': '35%',
                    'margin': 'auto',
                    'top': '15%'
                    },
            className = 'card text-white bg-info mb-3 bg-opacity-50 align-self-center'
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("User Saved")),
                dbc.ModalBody("Account creation success!", id='signup_confirmation'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", href='/'
                    )
                ),
            ],
            id="signup_modal",
            is_open=False,
        ),
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


# disable the signup button if passwords do not match
@app.callback(
    [
        Output('singup_signupbtn', 'disabled'),
    ],
    [
        Input('signup_password', 'value'),
        Input('signup_passwordconf', 'value'),
    ]
)
def deactivatesignup(password, passwordconf):
    
    # enable button if password exists and passwordconf exists 
    #  and password = passwordconf
    enablebtn = password and passwordconf and password == passwordconf

    return [not enablebtn]


# To save the user
@app.callback(
    [
        Output('signup_alert', 'is_open'),
        Output('signup_modal', 'is_open')   
    ],
    [
        Input('singup_signupbtn', 'n_clicks')
    ],
    [
        State('signup_username', 'value'),
        State('signup_password', 'value')
    ]
)
def saveuser(loginbtn, username, password):
    openalert = openmodal = False
    if loginbtn:
        if username and password:
            sql = """INSERT INTO users (user_name, user_password)
            VALUES (%s, %s)"""  
            
            # This lambda fcn encrypts the password before saving it
            # for security purposes, not even database admins should see
            # user passwords 
            encrypt_string = lambda string: hashlib.sha256(string.encode('utf-8')).hexdigest()  
            
            values = [username, encrypt_string(password)]
            db.modifydatabase(sql, values)
            
            openmodal = True
        else:
            openalert = True
    else:
        raise PreventUpdate

    return [openalert, openmodal]