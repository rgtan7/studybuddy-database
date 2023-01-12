from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.exceptions import PreventUpdate
import pandas as pd

from dash.dependencies import Input, Output, State

from app import app
from apps import dbconnect as db
from urllib.parse import urlparse, parse_qs



layout = html.Div(
    [
        html.Div(
          [
            dcc.Store(id='skills_toload', storage_type='memory', data=0),
          ],
        ),
        dbc.Card(
            [
                dbc.CardHeader ([html.H3("Expertise Details", style={'fontWeight': 'bold'})], className = "bg-info text-light"), 
                dbc.CardBody(
                    [
                        dbc.Row(
                        [
                            dbc.Label("Area of Expertise: ", width=2),
                            dbc.Col(
                            html.Div(
                                    dbc.Label(id = "skill_header"),
                                    className = "dash-bootstrap"
                                ),
                                width=2,
                            ),      
                        ],
                        className="mb-3",),
                        html.Hr(),
                        dbc.Row(
                        [
                            dbc.Label("Level: ", width=2),
                            dbc.Col(
                            html.Div(
                                    dbc.Label(id = "level_header"), 
                                    className = "dash-bootstrap"
                                ),
                                width=2,
                            ),      
                        ],
                        className="mb-3",),
                        html.Hr(),
                        dbc.Row(
                        [
                            dbc.Label("Number of Tutors Needed: ", width=2),
                            dbc.Col(
                            html.Div(
                                    dbc.Label(id = "number_header"), 
                                    className = "dash-bootstrap"
                                ),
                                width=2,
                            ),      
                        ],
                        className="mb-3",),
                        html.Hr(),
                    ]
                ), 
                dbc.CardFooter (
                    dbc.Row(
                        [
                            dbc.Col(dbc.Button('Edit AoE', id = 'modify_aoe', color = "warning" ),width =2, ),
                            dbc.Col(
                                dbc.Button('Add Skills', color="secondary", id = 'aoe_href'),
                                width=2, 
                                    #dbc.Button('View', href = f"/aoe/aoe_profile?mode=edit&id={aoeid}", size = 'sm', color = "warning"),
                            ), 
                        ], 
                       className="mb-3",
                    ), 
                )
                
            ]
        ),
        
        dbc.Card(
            [
                dbc.CardHeader([html.H5("Skills List", style={'fontWeight': 'bold'})], className = "bg-info text-light"),
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Search Skills", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="skills_name_filter", placeholder="Enter Filter"
                                            ),
                                        width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    "This will contain the table for skills", 
                                    id = 'skills_list',
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
    ]
)

@app.callback  (
    [
        Output('skill_header', 'children'),  
        Output('level_header', 'children'), 
        Output('modify_aoe', 'href'), 
        Output('number_header', 'children' ), 
        Output('aoe_href', 'href'), 
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search') 
    ]
)

def skill_view (pathname, search): 
    ctx = dash.callback_context
    parsed = urlparse(search)

    aoeid = parse_qs(parsed.query)['id'][0]

    href = f"/aoe/aoe_profile?mode=edit&id={aoeid}"
    aoehref = f'/skills_form?mode=add&id={aoeid}'
    
    if pathname == '/skills': 
        
            
        sqlcode = """ SELECT aoe_name, aoe_id, aoe_level, aoe_employeereq
        FROM aoe a
            INNER JOIN aoe_level l ON a.aoe_level_id = l.aoe_level_id
        ORDER BY aoe_id ASC 
        """
        parsed = urlparse(search)
        aoeid = parse_qs(parsed.query)['id'][0]
            
        val = ['aoeid']
        colnames = ['aoe', 'ID', 'aoe_level', 'aoe_employeereq']
        df = db.querydatafromdatabase(sqlcode, val, colnames)
        
     

        aoeidi = int(aoeid) -1
        aoe = df['aoe'][aoeidi]
        level = df['aoe_level'][aoeidi]
        number = df['aoe_employeereq'][aoeidi]

            
        return [aoe, level, href, number, aoehref]
    else: 
        raise PreventUpdate

@app.callback(
    [
        Output('skills_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('skills_name_filter', 'value'),
    ], 
    [
        State('url', 'search') 
    ]
)

def updateskilllist(pathname, searchterm, search):
    if pathname == '/skills':
        sql = """SELECT s.skill_name, s.skill_id, s.aoe_id FROM skill s
	        INNER JOIN aoe a ON s.aoe_id = a.aoe_id 
            WHERE NOT skill_delete_ind

        """
        val = []
        colnames = ['Skill', 'Skill_ID', 'AOE_ID']

        
        if searchterm:
            sql += """ AND skill_name ILIKE %s
            """
            val += [f"%{searchterm}%"]
        
        
        skills = db.querydatafromdatabase(sql, val, colnames)

        if skills.shape[0]:
            parsed = urlparse(search)
            id_caller = int(parse_qs(parsed.query)['id'][0])
            # print(id_caller)
            # print (skills['AOE_ID'][0])
            
            
            for aoeid in range (0, len(skills['AOE_ID'])): 
                if skills['AOE_ID'][aoeid] != id_caller: 
                    skills = skills.drop(aoeid)


                # skills = skills.drop(aoeid)
                
            #add buttons with the respective href
            buttons = []
            for aoeid in skills['Skill_ID']:
                buttons += [
                        html.Div(
                            dbc.Button('View', href = f"/skills_page?id={aoeid}", size = 'sm', color = "warning"), 
            #                 #href = f"/skills?id={aoeid}", 
            #                 #dbc.Button('View', href = f"/aoe/aoe_profile?mode=edit&id={aoeid}", size = 'sm', color = "warning"),
                            style = {'text-align':'center'}
                        )
                    ]
            skills['View'] = buttons
            
            skills.drop('AOE_ID', axis = 1, inplace=True)
            skills.drop('Skill_ID', axis = 1, inplace=True)
            
            table = dbc.Table.from_dataframe(skills, striped=True, bordered=True, hover=True, size = 'sm')
            return [table]
        else: 
            return["There are no records for that search term."]
    else: 
        raise PreventUpdate