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
            dcc.Store(id='aoe_toload', storage_type='memory', data=0),
          ],
        ),
        dbc.Row(
            [
                html.Img(src = '/assets/4.png', style = {'height' : '5%', 'width':'5%'}),
                dbc.Col(html.H2('Areas of Expertise')),
            ]
        ),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader([html.H3("Expertise List", style={'fontWeight': 'bold'})], className = "bg-info text-light"),
                dbc.CardBody(
                    [
                        dbc.Button('Add Expertise', color="secondary", href='/aoe/aoe_profile?mode=add'),
                        html.Hr(), 
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Search Area of Expertise", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="aoe_name_filter", placeholder="Enter Filter"
                                            ),
                                        width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    "This will contain the table for skills", 
                                    id = 'aoe_list',
                                )
                            ]
                        )
                    ]
                )
            ]
        ),   
    ],
)

@app.callback(
    [
        Output('aoe_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('aoe_name_filter', 'value'),
    ]        
    
)

def updateaoelist(pathname, searchterm):
    if pathname == '/aoe':
        
        
        sql_inquiry = """SELECT emp_id, emp.aoe_id, aoe_name 
            from emp  
                INNER JOIN aoe ON emp.aoe_id = aoe.aoe_id
            WHERE NOT emp_delete_ind
        """
                
        val = []
        colnames = ['empid', 'aoeid', 'aoename']
                
        emp_inquiry = db.querydatafromdatabase(sql_inquiry, val, colnames)

        unique_inqury = emp_inquiry.groupby('aoeid')['aoeid'].count().reset_index(name="count")
              
        sql_inquiry2 = """SELECT aoe_id, aoe_name, aoe_employeereq from aoe
        """
        val2 = [] 
        colnames = ['aoeid', 'aoename', 'required']
        aoe_inquiry = db.querydatafromdatabase(sql_inquiry2, val2, colnames)

                
        merged = pd.merge(unique_inqury, aoe_inquiry, how='right',  on = "aoeid")

                
        merged['count'] = merged['count'].fillna(0)
        merged['need'] = merged['required']- merged['count']
           
        values_s = [merged['count'], merged['need']]

        for i in range(len(merged)): 
            sqlcode_summary = """UPDATE aoe
            SET
                aoe_employeecount = %s, 
                aoe_employeeneed = %s 
            WHERE
                aoe_id = %s
            """
            values_s = [int(merged['count'][i]), int(merged['need'][i]), int(merged['aoeid'][i])]
            db.modifydatabase(sqlcode_summary, values_s)
        
        sql = """SELECT aoe_name, aoe_level, aoe_employeereq, aoe_employeecount, aoe_employeeneed, aoe_id
        
            FROM aoe a
                INNER JOIN aoe_level l ON a.aoe_level_id = l.aoe_level_id 
            WHERE NOT aoe_delete_ind
        """
        val = []
        colnames = ['AoE', 'Level', 'Required', 'Count', 'Need',  'ID']
        
        if searchterm:
            sql += """ AND aoe_name ILIKE %s
            """
            val += [f"%{searchterm}%"]
        
        aoes = db.querydatafromdatabase(sql, val, colnames)
        
        
        if aoes.shape[0]:
            # add buttons with the respective href
            buttons = []
            for aoeid in aoes['ID']:
                buttons += [
                        html.Div(
                            dbc.Button('View', href = f"/skills?id={aoeid}", size = 'sm', color = "warning"), 
                            style = {'text-align':'center'}
                        )
                    ]
            aoes['View'] = buttons
            
            aoes.drop('ID', axis = 1, inplace=True)
            
            table = dbc.Table.from_dataframe(aoes, striped=True, bordered=True, hover=True, size = 'sm')
            
            return [table]
        else: 
            return["There are no records for that search term."]
    else: 
        raise PreventUpdate
    
