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
            dcc.Store(id='skillspage_toload', storage_type='memory', data=0),
          ],
        ),
        dbc.Card(
            [
                dbc.CardHeader ([html.H3("Skill Details", style={'fontWeight': 'bold'})], className = "bg-info text-light"), 
                dbc.CardBody(
                    [
                        dbc.Row(
                        [
                            dbc.Label("Skill: ", width=2),
                            dbc.Col(
                            html.Div(
                                    dbc.Label(id = "skill_name"),
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
                                    dbc.Label(id = "skill_level_header"), 
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
                            dbc.Col(dbc.Button('Edit Skills', id = 'modify_skills', color = "warning"), width = 2), 
                           
                        ], 
                       className="mb-3",
                    ), 
                )
                
            ]
        ),
        
        dbc.Card(
            [
                dbc.CardHeader([html.H5("Employee List", style={'fontWeight': 'bold'})], className = "bg-info text-light"),
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Search Employee", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="employee_name_filter", placeholder="Enter Filter"
                                            ),
                                        width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    "This will contain the names of employees that have these skills", 
                                    id = 'employee_in_skills_list',
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
        Output('skill_name', 'children'),  
        Output('skill_level_header', 'children'), 
        Output('modify_skills', 'href'), 
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

    href = f"/skills_form?mode=edit&id={aoeid}"
    
    if pathname == '/skills_page': 
        
            
        sqlcode = """ SELECT skill_name, skill_id, aoe_level
        FROM skill s
            INNER JOIN aoe_level l ON s.aoe_level_id = l.aoe_level_id
        ORDER BY skill_id ASC 
        """
        parsed = urlparse(search)
        aoeid = parse_qs(parsed.query)['id'][0]
            
        val = ['aoeid']
        colnames = ['skill', 'ID', 'aoe_level']
        df = db.querydatafromdatabase(sqlcode, val, colnames)
        
     

        aoeidi = int(aoeid) - 1
        aoe = df['skill'][aoeidi]
        level = df['aoe_level'][aoeidi]
                    
        return [aoe, level, href]
    else: 
        raise PreventUpdate

@app.callback (
    [
        Output('employee_in_skills_list', 'children')
    ],
    [
        Input ('url', 'pathname'), 
        Input ('employee_name_filter', 'value')
    ],
    [
        State ('url', 'search')
    ]
)

def updateskillslist (pathname, searchterm, search):
    if pathname == '/skills_page': 
        sql_skill1 = """ SELECT emp_id, CONCAT(emp_name_first, ' ', emp_name_middle, ' ',  emp_name_last) as emp_Name, a.aoe_name, emp_sched, emp_phone, emp_email, s.skill_name, s.skill_id
        from emp 
            INNER JOIN skill s ON emp.skill_id_1 = s.skill_id
            INNER JOIN aoe a ON emp.aoe_id = a.aoe_id
        WHERE NOT emp_delete_ind  
        """
        sql_skill2 = """ SELECT emp_id, CONCAT(emp_name_first, ' ', emp_name_middle, ' ',  emp_name_last) as Emp_name, a.aoe_name, emp_sched, emp_phone, emp_email, s.skill_name, s.skill_id
        from emp 
            INNER JOIN skill s ON emp.skill_id_2 = s.skill_id
            INNER JOIN aoe a ON emp.aoe_id = a.aoe_id
        WHERE NOT emp_delete_ind  
        """
        
        sql_skill3 = """ SELECT emp_id, CONCAT(emp_name_first, ' ', emp_name_middle, ' ',  emp_name_last) as emp_name, a.aoe_name, emp_sched, emp_phone, emp_email, s.skill_name, s.skill_id
        from emp 
            INNER JOIN skill s ON emp.skill_id_3 = s.skill_id
            INNER JOIN aoe a ON emp.aoe_id = a.aoe_id
        WHERE NOT emp_delete_ind  
        """
        
        val = []
        colname = ['EmpID', 'Name', 'AoE', 'Availability', 'Phone', 'Email', 'Skill', 'SkillID']
        
        if searchterm: 
            sql_skill1 += """ AND CONCAT(emp_name_first, ' ', emp_name_middle, ' ',  emp_name_last) ILIKE %s
            """
            sql_skill2 += """ AND CONCAT(emp_name_first, ' ', emp_name_middle, ' ',  emp_name_last) ILIKE %s
            """
            sql_skill3 += """ AND CONCAT(emp_name_first, ' ', emp_name_middle, ' ',  emp_name_last) ILIKE %s
            """
            val += [f"%{searchterm}%"]
        
        employees = db.querydatafromdatabase(sql_skill1, val, colname)
        employees = employees.append(db.querydatafromdatabase(sql_skill2, val, colname))
        employees = employees.append(db.querydatafromdatabase(sql_skill3, val, colname))
        print (len(employees))
        employees.reset_index(drop=True, inplace = True )
        
        print(employees)
        
        if employees.shape[0]:
            # add buttons with the respective href
            parsed = urlparse(search)
            id_caller = int(parse_qs(parsed.query)['id'][0])
            buttons = []
            dfcount = 0
            for skillid in employees['SkillID']:
                
                if skillid != id_caller: 
                    employees = employees.drop(dfcount)
                dfcount += 1
                
            for empID in employees['EmpID']:
                    buttons += [
                            html.Div(
                                dbc.Button('View/Edit', href = f"/directory/directory_profile?mode=edit&id={empID}", size = 'sm', color = "warning"), 
                                style = {'text-align':'center'}
                            )
                    ]
            
            print(employees)
            employees['View/Edit'] = buttons
            employees.drop('EmpID', axis = 1, inplace=True)
            employees.drop('Skill', axis = 1, inplace=True)
            employees.drop('SkillID', axis = 1, inplace=True)
            table = dbc.Table.from_dataframe(employees, striped=True, bordered=True, hover=True, size = 'sm')
            return [table]
        else: 
            return ["There are no records for that search term."]
    else:
        raise PreventUpdate