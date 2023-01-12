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
            dcc.Store(id='addequipmentpage_toload', storage_type='memory', data=0),
          ],
        ),

        html.Hr(),

        dbc.Card([
            dbc.CardHeader([html.Hr(), html.H3("Equipment Lending Form", style={'fontWeight': 'bold'}), html.Hr()], className = "bg-info text-light"),
        ], style = {'width': '60%', 'margin': 'auto'}),

        dbc.Card([
            dbc.CardBody([
                dbc.Row(
                    [
                        dbc.Label("Equipment Name", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type="text", id="equipment_name", placeholder="Enter Equipment"
                                ),
                                width=6,
                            ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Equipment Type", width=2),
                            dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                        id='equipment_type',
                                        clearable=True,
                                        searchable=True, 
                                        options=[
                                            dict(label='SOFTWARE',value='SOFTWARE'),
                                            dict(label='HARDWARE',value='HARDWARE')
                                        ]
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
                        dbc.Label("Lent To", width=2),
                            dbc.Col(
                                html.Div(
                                dcc.Dropdown(
                                        id='equipment_lend',
                                        clearable=True,
                                        searchable=True,
                                    ), 
                                    className = "dash-bootstrap"
                                ),
                                width=6,
                            ),
                    ],
                    className="mb-3",
                ),
            ])
        ], style = {'width': '60%', 'margin': 'auto'}),

        html.Hr(),

        dbc.Card([
            dbc.CardBody([
                html.Div(
                    dbc.Row(
                        [
                            dbc.Label("Delete?", width=2),
                            dbc.Col(
                                dbc.Checklist(
                                    id='equipment_removerecord',
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
                    id='equipment_removerecord_div'
                ),
                dbc.Button('Submit', color="success", id = 'equipment_submitbtn'),                
            ])
        ], style = {'width': '60%', 'margin': 'auto'}),

        html.Hr(),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("tempmessage", id = 'equipment_feedback_message')),
                #dbc.ModalBody("tempmessage", id = 'equipment_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="equipment_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="equipment_modal",
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
        Output('equipment_lend', 'options'),  
        Output('addequipmentpage_toload', 'data'),
        Output('equipment_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search') 
    ]
)

def lendoptions_leveldropdown (pathname, search): 
    if pathname == '/equipment/equipment_profile':
        
        if pathname == '/equipment/equipment_profile':
            
            sql = """ SELECT CONCAT(emp.emp_name_first , ' ' , emp.emp_name_middle, ' ', emp.emp_name_last) AS label, emp_id as value
                FROM emp

            WHERE NOT emp_delete_ind
            """
            values = [] 
            
            cols = ['label', 'value']
            
            

            df = db.querydatafromdatabase(sql, values, cols)
            
            lendto_opts = df.to_dict('records')
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            to_load = 1 if mode == 'edit' else 0
            removerecord_div = None if to_load else {'display':'none'}
    else: 
        raise PreventUpdate
    return [lendto_opts, to_load, removerecord_div]

@app.callback(
    [
        Output('equipment_modal', 'is_open'),
        Output('equipment_feedback_message', 'children'),
        Output('equipment_closebtn', 'href'),
    ], 
    [
        Input ('equipment_submitbtn', 'n_clicks'),
        Input('equipment_closebtn', 'n_clicks')
    ], 
    [
        State('equipment_name', 'value'), 
        State('equipment_type', 'value'), 
        State('equipment_lend', 'value'), 
        State ('url', 'search'), 
        State ('equipment_removerecord', 'value')
    ]
    
)

def equipmentlend_submitprocess(submitbtn, closebtn, name, type, lend, search, removerecord): 
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ' '
        okay_href = None
    else: 
        raise PreventUpdate
    
    if eventid == 'equipment_submitbtn' and submitbtn: 
        openmodal = True 
        inputs = [ 
                  name,
                  type, 
                  lend 
                ]
        if not all(inputs): 
            feedbackmessage = "Please supply all inputs."
        elif len(name) > 256: 
            feedbackmessage = "Equipment name is too long (length > 256)"
        else: 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            
            if mode == 'add': 
                sqlcode = """ INSERT INTO equipment (
                    equipment_name, 
                    equipment_type, 
                    emp_id, 
                    equipment_delete_ind 
                )
                VALUES (%s, %s, %s, %s)
                """ 
                values = [name, type, lend, False]
                db.modifydatabase(sqlcode, values)
                feedbackmessage = "Saved to database."
                okay_href = '/equipment'
            
            elif mode == 'edit': 
                parsed = urlparse(search)
                equipmentid = parse_qs(parsed.query)['id'][0]
                
                sqlcode = """UPDATE equipment 
                SET 
                    equipment_name = %s, 
                    equipment_type = %s, 
                    emp_id = %s, 
                    equipment_delete_ind = %s
                WHERE 
                    equipment_id = %s  
                """
                
                to_delete = bool(removerecord)
                values = [name, type, lend, to_delete, equipmentid]
                db.modifydatabase(sqlcode, values)
                
                feedbackmessage = "Equipment Lending Database Updated."
                okay_href = '/equipment'
            else: 
                raise PreventUpdate
    elif eventid == 'equipment_closebtn' and closebtn: 
        pass 
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href ]
            

@app.callback (
    [
        Output('equipment_name', 'value'), 
        Output('equipment_type', 'value'), 
        Output('equipment_lend', 'value'), 
    ], 
    [
        Input('addequipmentpage_toload', 'modified_timestamp')
    ],
    [
        State('addequipmentpage_toload', 'data'), 
        State('url', 'search'), 
    ]
)

def loadequipmentlendpage(timestamp, to_load, search): 
    if to_load == 1: 
        sql = """ SELECT equipment_name, equipment_type, emp_id 
        FROM equipment 
        WHERE equipment_id = %s 
        """
        
        parsed = urlparse(search)
        equipmentid = parse_qs(parsed.query)['id'][0]
        
        val = [equipmentid]
        colnames = ['equipment_name', 'equipment_type', 'emp_name']
        
        df = db.querydatafromdatabase(sql, val, colnames)
        
        equipment_name = df['equipment_name'][0]
        equipment_type = df['equipment_type'][0]
        employee_name = df['emp_name'][0] 
        
        return [equipment_name, equipment_type, employee_name]
    else: 
        raise PreventUpdate       

