from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app

from apps import dbconnect as db
from urllib.parse import urlparse, parse_qs


layout = html.Div(
    [
        html.Div(
          [
            dcc.Store(id='addaoepage_toload', storage_type='memory', data=0),
          ],
        ),

        html.Hr(),

        dbc.Card([
            dbc.CardHeader([html.Hr(), html.H3("Area of Expertise Form", style={'fontWeight': 'bold'}), html.Hr()], className = "bg-info text-light"),
        ], style = {'width': '60%', 'margin': 'auto'}),

        dbc.Card([
            dbc.CardBody([
                dbc.Row(
                    [
                        dbc.Label("Area of Expertise", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type="text", id="aoe_title", placeholder="Enter Area of Expertise"
                                ),
                                width=6,
                            ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Level", width=2),
                            dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                        id = 'aoe_level',
                                        clearable =True, 
                                        searchable = True, 
                                        disabled = False, 
                                        
                                    ), 
                                    className = "dash-bootstrap"
                                ),
                                width=6,
                            ),      
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Number of Tutors Needed", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type="int", id="aoe_numbersneed", placeholder="Enter Number of Employees Needed"
                                ),
                                width=6,
                            ),
                    ],
                    className="mb-3",
                ),
            ])
        ], style = {'width': '60%', 'margin': 'auto'}),

        html.Hr(),

        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(
                                dbc.Row(
                                    [
                                        dbc.Label("Delete?", width=2),
                                        dbc.Col(
                                            dbc.Checklist(
                                                id='aoe_removerecord',
                                                value = [],
                                                options=[
                                                    {
                                                        'label': "Mark for Deletion",
                                                        'value': 1
                                                    }
                                                ],
                                                style={'fontWeight':'bold'},
                                            ),
                                            width=6,
                                        ),      
                                    ],
                                    className="mb-3",
                                ),
                                id='aoe_removerecord_div'
                            ),
                            dbc.Button('Submit', color="success", id = 'aoe_submitbtn'),
                    ])
            ], style = {'width': '60%', 'margin': 'auto'}
        ),

        html.Hr(),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("tempmessage", id = 'aoe_feedback_message')),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="aoe_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="aoe_modal",
            is_open=False,
        ),
    ],
    style = {'background-image': 'url("/assets/white bg.jpg")',
    'background-attachment': 'fixed',
    'background-repeat': 'repeat',
    'width': '100%',
    'position': 'absolute'}
)

@app.callback(
    [
        Output('aoe_level', 'options'),  
        Output('addaoepage_toload', 'data'),
        Output('aoe_removerecord_div', 'style'),
        Output('aoe_level', 'disabled'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search') 
    ]
)

def aoe_leveldropdown (pathname, search): 
    if pathname == '/aoe/aoe_profile':
        
        if pathname == '/aoe/aoe_profile':
            
            sql = """ SELECT  
                aoe_level as label, aoe_level_id as value 
                FROM aoe_level 
            """ 
            values = [] 
            
            cols = ['label', 'value']
            df = db.querydatafromdatabase(sql, values, cols)
            
            aoe_level_options = df.to_dict('records')
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            to_load = 1 if mode == 'edit' else 0
            removerecord_div = None if to_load else {'display':'none'}
            disabled = False if mode == 'add' else True
    else: 
        raise PreventUpdate
    return [aoe_level_options, to_load, removerecord_div, disabled]

@app.callback(
    [
        Output('aoe_modal', 'is_open'),
        Output('aoe_feedback_message', 'children'),
        Output('aoe_closebtn', 'href'),
    ],
    [
        Input('aoe_submitbtn', 'n_clicks'),
        Input('aoe_closebtn', 'n_clicks')
    ],
    [
        State('aoe_title', 'value'),
        State('aoe_level', 'value'),
        State('aoe_numbersneed', 'value'),
        State('url', 'search'),
        State('aoe_removerecord', 'value')
    ]
)

def aoe_submitprocess(submitbtn, closebtn, title, level, tutorsneed, search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ' '
        okay_href = None
    else: 
        raise PreventUpdate
    
    if eventid == 'aoe_submitbtn' and submitbtn: 
        openmodal = True
        
        #check for inputs
        inputs = [ 
                title, 
                level, 
                tutorsneed
                ]
        #if error raise prompt 
        if not all (inputs): 
            feedbackmessage = "Please supply all inputs."
        elif len(title) > 256: 
            feedbackmessage = "AoE is too long (length >256)"
        # else save to db 
        else: 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            
            if mode == "add": 
                sqlcode = """ INSERT INTO aoe(
                    aoe_name, 
                    aoe_level_id, 
                    aoe_employeereq, 
                    aoe_delete_ind
                )
                VALUES(%s, %s,%s,%s)
                """
                
                values = [title, level, tutorsneed, False]
                db.modifydatabase(sqlcode, values)
                #save to db
                feedbackmessage = "AoE saved to database."
                okay_href = '/aoe'
                
            elif mode == 'edit': 
                parsed = urlparse(search)
                aoeid = parse_qs(parsed.query)['id'][0]
                
                sqlcode = """UPDATE aoe
                SET
                    aoe_name = %s, 
                    aoe_level_id = %s, 
                    aoe_employeereq = %s,
                    aoe_delete_ind = %s
                WHERE
                    aoe_id = %s
                """
                
                to_delete = bool(removerecord)
                values = [title, level, tutorsneed, to_delete, aoeid]
                db.modifydatabase(sqlcode, values)
                
                feedbackmessage = "AOE updated to database."
                okay_href = '/aoe'
            else: 
                raise PreventUpdate
        
        
    elif eventid == 'aoe_closebtn' and closebtn:
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href]

@app.callback(
    [
        Output('aoe_title', 'value'),
        Output('aoe_level', 'value'),
        Output('aoe_numbersneed', 'value'),
    ],
    [
        Input('addaoepage_toload', 'modified_timestamp'),
    ], 
    [
        State('addaoepage_toload', 'data'),
        State('url', 'search'),
    ]
)

def loadmoviedetails(timestamp, to_load, search): 
    if to_load == 1: 
        #1 query the movie details from the database 
        sql = """SELECT aoe_name, aoe_level_id, aoe_employeereq
        FROM aoe
        WHERE aoe_id = %s
        """
        
        parsed = urlparse(search)
        aoeid = parse_qs(parsed.query)['id'][0]
        
        val = [aoeid]
        colnames = ['aoe', 'level', 'employeereq']
        
        
        df = db.querydatafromdatabase(sql, val, colnames)
        #2 load the values to interface
        
        aoe = df['aoe'][0]
        level = df['level'][0]
        employeereq = df['employeereq'][0]
        
        return  [aoe,  level, employeereq]
    else: 
        raise PreventUpdate