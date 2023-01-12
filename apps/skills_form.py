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
            dcc.Store(id='addskillspage_toload', storage_type='memory', data=0),
          ],
        ),

        html.Hr(),

        dbc.Card([
            dbc.CardHeader([html.Hr(), html.H3("Skills Form", style={'fontWeight': 'bold'}), html.Hr()], className = "bg-info text-light"),
        ], style = {'width': '60%', 'margin': 'auto'}),


        dbc.Card([
            dbc.CardBody([
                dbc.Row(
                    [
                        dbc.Label("Skill", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type="text", id="skills_title", placeholder="Enter Skill"
                                ),
                                width=6,
                            ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("AoE", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type = "text", id = 'AoE_here', readonly= 1
                                ), 
                                width = 6, 
                                ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Level", width=2),
                            dbc.Col(
                            dbc.Input(
                                    type = "text", id = 'skill_level', readonly= 1
                                ), 
                                width = 6, 
                            ),      
                    ],
                    className="mb-3",
                ),
            ])
        ], style = {'width': '60%', 'margin': 'auto'}),

        html.Hr(),

        dbc.Card(
            [
                dbc.CardBody([
                    html.Div(
                        dbc.Row(
                            [
                                dbc.Label("Delete?", width=2),
                                dbc.Col(
                                    dbc.Checklist(
                                        id='skill_removerecord',
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
                        id='skill_removerecord_div'
                    ),
                    dbc.Button('Submit', color="success", id = 'skill_submitbtn'),
                ])                
            ], style = {'width': '60%', 'margin': 'auto'}
        ),

        html.Hr(),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("tempmessage", id = 'skill_feedback_message')),
                #dbc.ModalBody("tempmessage", id = 'skill_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="skill_closebtn", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="skill_modal",
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
        Output('skills_title', 'value'), 
        Output('AoE_here', 'value'), 
        Output('skill_level', 'value'),
        Output('addskillspage_toload', 'data'),
        Output('skill_removerecord_div', 'style'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search') 
    ]
)

def aoe_nameforce (pathname, search): 
    if pathname == '/skills_form':
        parsed = urlparse(search)
        mode = parse_qs(parsed.query)['mode'][0]
        aoeid = parse_qs(parsed.query)['id'][0]
        aoeid_int = int(aoeid)
        if pathname == '/skills_form':
            if mode == 'add': 
                
                ctx = dash.callback_context
                
                
                sqlaoe = """ SELECT  
                    a.aoe_name as name_aoe, a.aoe_id as aoe_value, l.aoe_level as aoelevel
                    FROM aoe a
                        INNER JOIN aoe_level l ON a.aoe_level_id = l.aoe_level_id 
                    ORDER BY aoe_id ASC
                """ 
                aoe_values = [] 
                
                aoe_cols = ['name_aoe', 'aoe_value', 'aoelevel']
                dfaoe = db.querydatafromdatabase(sqlaoe, aoe_values, aoe_cols)
                
                aoe_name_options = dfaoe.to_dict('records')

                aoe_name_options_forced = aoe_name_options[aoeid_int - 1]['name_aoe']
                aoe_level_options_forced = aoe_name_options[aoeid_int- 1]['aoelevel']
                skill_name_foced = ''
                
                to_load = 1 if mode == 'edit' else 0
                removerecord_div = None if to_load else {'display':'none'}

            
            elif mode =='edit': 
                ctx = dash.callback_context
                
                sql = '''SELECT 
                s.skill_name as skill,  a.aoe_name as aoe, l.aoe_level as aoe_level
                FROM skill s
                    INNER JOIN aoe_level l ON s.aoe_level_id = l.aoe_level_id
                    INNER JOIN aoe a ON s.aoe_id = a.aoe_id
                ORDER BY skill_id ASC
                
                ''' 
                
                skill_values = [] 
                
                skill_cols = ['skill', 'aoe', 'aoe_level']
                df = db.querydatafromdatabase(sql, skill_values, skill_cols)
                aoe_name_options = df.to_dict('records')
                aoe_name_options_forced = aoe_name_options[aoeid_int - 1]['aoe']
                aoe_level_options_forced = aoe_name_options[aoeid_int - 1]['aoe_level']
                skill_name_foced = aoe_name_options[aoeid_int - 1]['skill']
                to_load = 1 if mode == 'edit' else 0
                removerecord_div = None if to_load else {'display':'none'}
                
            else: 
                raise PreventUpdate
        
        
    else: 
        raise PreventUpdate
    return [skill_name_foced, aoe_name_options_forced, aoe_level_options_forced, to_load, removerecord_div]

@app.callback(
    [
        Output('skill_modal', 'is_open'),
        Output('skill_feedback_message', 'children'),
        Output('skill_closebtn', 'href'),
    ],
    [
        Input('skill_submitbtn', 'n_clicks'),
        Input('skill_closebtn', 'n_clicks')
    ],
    [
        State('skills_title', 'value'),
        State('AoE_here', 'value'),
        State('skill_level', 'value'),
        State('url', 'search'),
        State('skill_removerecord', 'value')
    ]
)

def aoe_submitprocess(submitbtn, closebtn, skill, aoe, level, search, removerecord):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ' '
        okay_href = None
    else: 
        raise PreventUpdate
    
    if eventid == 'skill_submitbtn' and submitbtn: 
        openmodal = True
        
        #check for inputs
        inputs = [ 
                skill, 
                aoe, 
                level
                ]
        #if error raise prompt 
        if not all (inputs): 
            feedbackmessage = "Please supply all inputs."
        elif len(skill) > 256: 
            feedbackmessage = "Skill name is too long (length >256)"
        # else save to db 
        else: 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            
            if mode == "add": 
                aoeid = parse_qs(parsed.query)['id'][0]
                aoeid_int = int(aoeid)
                sqlcode = """ INSERT INTO skill(
                    skill_name, 
                    aoe_id, 
                    aoe_level_id, 
                    skill_delete_ind, 
                    skill_id
                )
                VALUES(%s,%s,%s,%s,%s)
                
                """
                
                sql_level = """ SELECT 
                aoe_level_id, aoe_id
                FROM aoe a
                ORDER BY aoe_id ASC
                """
                aoe_level = [] 
                
                aoe_cols = ['aoe_level_id', 'aoe_id']
                df = db.querydatafromdatabase(sql_level, aoe_level, aoe_cols)
                aoe_levels = df.to_dict('records')
                
                sql_skill = """ SELECT 
                skill_id
                FROM skill 
                """
                
                skill_level = []
                skill_cols = ['skill_id']
                df_skill = db.querydatafromdatabase(sql_skill, skill_level, skill_cols )
                skill_datab =df_skill.to_dict('records')
                
                

                aoe_level_forced = aoe_levels[aoeid_int-1]['aoe_level_id']
                skill_id_iter = len(skill_datab)+ 1

                
            
                values = [skill, aoeid, aoe_level_forced, False, skill_id_iter]
                db.modifydatabase(sqlcode, values)
                #save to db
                feedbackmessage = "Skill saved to database."
                okay_href = f'/skills?id={aoeid}'
                
            elif mode == 'edit': 
                aoeid = parse_qs(parsed.query)['id'][0]
                aoeid_int = int(aoeid)
                
                parsed = urlparse(search)
                aoeid = parse_qs(parsed.query)['id'][0]
                
                sqlcode = """UPDATE skill
                SET
                    skill_name = %s, 
                    aoe_id  = %s, 
                    aoe_level_id = %s,
                    skill_delete_ind = %s
                WHERE
                    skill_id = %s
                
                """
                
                # DELETE FROM skill s 
                # WHERE skill_delete_ind = True 
                
                sql_skill = """ SELECT 
                skill_name, aoe_id, aoe_level_id 
                FROM skill 
                """
                
                edit_skill = []
                edit_skill_cols = ['skill_name', 'aoe_id', 'aoe_level_id']
                df = db.querydatafromdatabase(sql_skill, edit_skill, edit_skill_cols)
                skill_df = df.to_dict('records')
                level_forced = skill_df[aoeid_int - 1]['aoe_level_id']
                aoe_forced = skill_df[aoeid_int - 1]['aoe_id']
                int_aoe_forced = int(aoe_forced)
                
                
                to_delete = bool(removerecord)
                values = [skill, aoe_forced, level_forced, to_delete, aoeid]
                db.modifydatabase(sqlcode, values)
                
                feedbackmessage = "Skill updated to database."
                okay_href = f'/skills?id={int_aoe_forced}'
            else: 
                raise PreventUpdate
        
        
    elif eventid == 'skill_closebtn' and closebtn:
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href ]
