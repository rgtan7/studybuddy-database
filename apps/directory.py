from platform import release
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import pandas as pd
from urllib.parse import urlparse, parse_qs

from app import app
from apps import dbconnect as db



layout = html.Div(
    [
        dbc.Row(
            [
                html.Img(src = '/assets/3.png', style = {'height' : '5%', 'width':'5%'}),
                dbc.Col(html.H2('Directory')),
            ]
        ),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader([html.H3("Employee List", style={'fontWeight': 'bold'})], className = "bg-info text-light"),      
                dbc.CardBody(
                    [
                        dbc.Button("Add Employee", color="secondary", href='/directory/directory_profile?mode=add'),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Search for an Employee", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="employee_name_filter", placeholder="Enter Filter"
                                            ), width=6
                                        ),
                                    ], className="mb-3"
                                ),
                                html.Div(
                                    "This will contain the table for employees",
                                    id='directory_employeelist',
                                    
                                ),
                            ]
                        )
                    ]
                ),
            ]
        )
    ]
)

@app.callback(
    [
        Output('directory_employeelist', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('employee_name_filter', 'value'),
    ]
)
def updateemployeelist(pathname, searchterm):
    if pathname == '/directory':
        sql = """SELECT CONCAT(emp_name_last, ', ', emp_name_first, ' ', LEFT(emp_name_middle, 1)) AS emp_Name,  CONCAT (aoe_name,'-' ,aoe_level ) as aoe_name, emp_sched, emp_phone, emp_email, emp_id
        
            FROM emp
                INNER JOIN aoe ON emp.aoe_id = aoe.aoe_id
                INNER JOIN aoe_level al ON aoe.aoe_level_id = al.aoe_level_id

            WHERE NOT emp_delete_ind
        """
        val = []
        colnames = ['Name', 'AoE', 'Availability', 'Phone Number',   'E-mail','ID']
        
        if searchterm:
            sql += """ AND CONCAT(emp_name_last, ', ', emp_name_first, ' ', LEFT(emp_name_middle, 1))  ILIKE %s
            """
            val += [f"%{searchterm}%"] 
        
        employees = db.querydatafromdatabase(sql, val, colnames)

        if employees.shape[0]:
            # add buttons with the respective href
            buttons = []
            for employeeid in employees['ID']:
                buttons += [
                        html.Div(
                            dbc.Button('View/Edit', href = f"/directory/directory_profile?mode=edit&id={employeeid}", size = 'sm', color = "warning"), 
                            style = {'text-align':'center'}
                        )
                    ]
            employees['Action'] = buttons
            
            employees.drop('ID', axis = 1, inplace=True)
            
            table = dbc.Table.from_dataframe(employees, striped=True, bordered=True, hover=True, size = 'sm')
            return [table]
        else: 
            return["There are no records for that search term."]
    else: 
        raise PreventUpdate



