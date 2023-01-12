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
            dcc.Store(id='equipment_toload', storage_type='memory', data=0),
          ],
        ),
        dbc.Row(
            [
                html.Img(src = '/assets/5.png', style = {'height' : '5%', 'width':'5%'}),
                dbc.Col(html.H2('Equipment Lending')),
            ]
        ),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardHeader([html.H3("Equipment List", style={'fontWeight': 'bold'})], className = "bg-info text-light"),
                dbc.CardBody(
                    [
                        dbc.Button('Lend Equipment', color="secondary", href='/equipment/equipment_profile?mode=add'),
                        html.Hr(), 
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Search for Equipment", width=2),
                                        dbc.Col(
                                            dbc.Input(
                                                type="text", id="equipment_name_filter", placeholder="Enter Filter"
                                            ),
                                        width=6,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    "This will contain the table for equipment", 
                                    id = 'equipment_list',
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        
    ]
)

@app.callback(
    [
        Output('equipment_list', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('equipment_name_filter', 'value'),
    ]        
    
)

def updateequipmentlist(pathname, searchterm):
    if pathname == '/equipment':
        sql = """SELECT equipment_name, equipment_type,  CONCAT(emp_name_last, ', ', emp_name_first, ' ', LEFT(emp_name_middle, 1), '.') AS emp_Name,  equipment_id
        
            FROM equipment 
                INNER JOIN emp  ON equipment.emp_id = emp.emp_id 
            WHERE NOT equipment_delete_ind
        """
        val = []
        colnames = ['Equipment', 'Type', 'Lent To', 'ID']
        
        if searchterm:
            sql += """ AND equipment_name ILIKE %s
            """
            val += [f"%{searchterm}%"]
        
        
        equipments = db.querydatafromdatabase(sql, val, colnames)

        if equipments.shape[0]:
            # add buttons with the respective href
            buttons = []
            for equipmentid in equipments['ID']:
                buttons += [
                        html.Div(
                            dbc.Button('View/Edit', href = f"/equipment/equipment_profile?mode=edit&id={equipmentid}", size = 'sm', color = "warning"), 
                            style = {'text-align':'center'}
                        )
                    ]
            equipments['Action'] = buttons
            
            equipments.drop('ID', axis = 1, inplace=True)
            
            table = dbc.Table.from_dataframe(equipments, striped=True, bordered=True, hover=True, size = 'sm')
            return [table]
        else: 
            return["There are no records for that search term."]
    else: 
        raise PreventUpdate
