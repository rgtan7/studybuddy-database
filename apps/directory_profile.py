from pickle import FALSE
from turtle import right
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from urllib.parse import urlparse, parse_qs
from apps import dbconnect as db
from app import app



layout = html.Div(
    [
        html.Div(
            [
                dcc.Store(id='directoryprof_toload', storage_type='memory', data=0),
            ]
        ),
        html.Hr(),
        dbc.Card([
            dbc.CardHeader([html.Hr(), html.H3("Employee Form", style={'fontWeight': 'bold'}), html.Hr()], className = "bg-info text-light"),
        ], style = {'width': '60%', 'margin': 'auto'}),
        dbc.Card([
            dbc.CardHeader([html.H5("Personal Information", style={'fontWeight': 'bold'})], className = "bg-secondary text-light"),
            dbc.CardBody([
                dbc.Row(
                    [
                        dbc.Label("Last Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", 
                                id="emp_name_last", 
                                placeholder="Enter Surname"
                            ),
                            width=6
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("First Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", 
                                id="emp_name_first", 
                                placeholder="Enter First Name"
                            ),
                            width=6
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Middle Name", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", 
                                id="emp_name_middle", 
                                placeholder="Enter Middle Name"
                            ),
                            width=6
                        ),
                    ],
                    className="mb-3",
                ),   
                dbc.Row(
                    [
                        dbc.Label("Sex at Birth", width=2),
                        dbc.Col(
                        dcc.Dropdown(
                                        id='emp_sex',
                                        searchable=True,
                                        options=[
                                            dict(label='Male',value='Male'),
                                            dict(label='Female',value='Female')
                                        ]
                                    ),
                                width=3,
                            ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Birthdate", width=2),
                            dbc.Col(
                                dcc.DatePickerSingle(
                                id='emp_bday',
                                ),
                                width=6,
                            ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Civil Status", width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                        id='emp_civil',
                                        searchable=True,
                                        options=[
                                            dict(label='Single',value='Single'),
                                            dict(label='Married',value='Married'),
                                            dict(label='Widowed', value='Widowed'),
                                            dict(label='Separated',value='Separated')
                                        ]
                                    ),
                                width=3,
                            ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Highest Educational Attainment", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", 
                                id="emp_degree", 
                                placeholder="Enter Degree"
                            ),
                            width=6
                        ),
                    ],
                    className="mb-3",
                ),
            ])
        ],style = {'width': '60%', 'margin': 'auto'}),
        dbc.Card([ 
            dbc.CardHeader([html.H5("Contact Details", style={'fontWeight': 'bold'})], className = "bg-secondary text-light"),
            dbc.CardBody([
                html.H6("Contact Information"),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Label("Phone Number", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="int", 
                                id="emp_phone", 
                                placeholder="Enter Phone Number"
                            ),
                            width=6
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("E-mail Address", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", 
                                id="emp_email", 
                                placeholder="Enter E-mail Address"
                            ),
                            width=6
                        ),
                    ],
                    className="mb-3",
                ),
                html.Hr(),
                html.H6("Address"),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Label("HouseNo, Street/Unit ", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", 
                                id="emp_address1", 
                                placeholder="Enter Address Line 1"
                            ),
                            width=6
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Village, Barangay/County", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", 
                                id="emp_address2", 
                                placeholder="Enter Address Line 2"
                            ),
                            width=6
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("City/Town, Province)", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", 
                                id="emp_address3", 
                                placeholder="Enter Address Line 3"
                            ),
                            width=6
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Country", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="text", 
                                id="emp_address4", 
                                placeholder="Enter Address Line 4"
                            ),
                            width=6
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Postal Code", width=2),
                        dbc.Col(
                            dbc.Input(
                                type="int", 
                                id="emp_postal", 
                                placeholder="Enter Postal Code"
                            ),
                            width=6
                        ),
                    ],
                    className="mb-3",
                ),
            ]),
            dbc.Card ([
                dbc.CardHeader([html.H5("Hiring Details", style={'fontWeight': 'bold'})], className = "bg-secondary text-light"),
                dbc.CardBody([
                dbc.Row(
                    [
                        dbc.Label("Area of Expertise", width=2),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='aoe_name',
                                    clearable=True,
                                    searchable=True, persistence= True, persistence_type= 'memory'
                                ),  
                                className="dash-bootstrap"
                            )
                        )
                    ],
                    className="mb-3",
                ),
                html.Div(
                    dbc.Row(
                    [
                        dbc.Label("Skill 1", width=2),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                        id='aoe_skills1',
                                        clearable=True,
                                        searchable=True
                                    ),
                                className="dash-bootstrap"
                            )
                        ),      
                    ],
                        className="mb-3",
                    ), id = 'skill_1div' 
                ),
                html.Div(
                    dbc.Row(
                    [
                        dbc.Label("Skill 2", width=2),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                        id='aoe_skills2',
                                        clearable=True,
                                        searchable=True
                                    ),
                                className="dash-bootstrap"
                            )
                        ),      
                    ],
                        className="mb-3",
                    ), id = 'skill_2div', style = {'display':'none'}
                ),
                html.Div(
                    dbc.Row(
                    [
                        dbc.Label("Skill 3", width=2),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                        id='aoe_skills3',
                                        clearable=True,
                                        searchable=True
                                    ),
                                className="dash-bootstrap"
                            )
                        ),      
                    ],
                        className="mb-3",
                    ), id = 'skill_3div', style = {'display':'none'}
                ),
                dbc.Row(
                    [
                        dbc.Label("Hire Date", width=2),
                            dbc.Col(
                                dcc.DatePickerSingle(
                                id='emp_hiredate',
                                ),
                                width=6,
                            ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        dbc.Label("Availability", width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                        id='emp_sched',
                                        searchable=True,
                                        options=[
                                            dict(label='Available',value='Available'),
                                            dict(label='Not Available',value='Not Available'),
                                        ]
                                    ),
                                width=3,
                            ),
                    ],
                ), 
                ]),
            ]),
            dbc.Card ([
                dbc.CardHeader([html.H5("Banking Information", style={'fontWeight': 'bold'})], className = "bg-secondary text-light"),
                dbc.CardBody([
                    dbc.Row(
                        [
                            dbc.Label("Bank Name", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type="text", 
                                    id="emp_bank", 
                                    placeholder="Enter Bank Name"
                                ),
                                width=6
                            ),
                        ],
                        className="mb-3",
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Bank Account Name", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type="text", 
                                    id="emp_bank_name", 
                                    placeholder="Enter Bank Account Name"
                                ),
                                width=6
                            ),
                        ],
                        className="mb-3",
                    ),
                    dbc.Row(
                        [
                            dbc.Label("Bank Account Number", width=2),
                            dbc.Col(
                                dbc.Input(
                                    type="int", 
                                    id="emp_bank_num", 
                                    placeholder="Enter Bank Account Number"
                                ),
                                width=6
                            ),
                        ],
                        className="mb-3",
                    ),
                ],),
            ],), 
        ], style = {'width': '60%', 'margin': 'auto'}),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(
                            dbc.Row(
                                [
                                    dbc.Label("Wish to delete?", width=3),
                                    dbc.Col(
                                        dbc.Checklist(
                                            id='directoryprof_removerecord',
                                            options=[
                                                {
                                                    'label': "Mark for Deletion",
                                                    'value': 1
                                                }
                                            ],
                                            style={'fontWeight':'bold'},
                                        ),
                                        width=6
                                    ),
                                ],
                                className="mb-3",
                            ),
                            id='directoryprof_removerecord_div'
                        ),
                        dbc.Button("Submit", color="success", id='directoryprof_submitbtn', n_clicks=0, style = {'margin': 'auto'}),
                    ]
                )
            ],
            style = {'width': '60%', 'margin': 'auto'}
        ),

        html.Hr(),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Tempmessage", id='directoryprof_feedback_message')),
                #dbc.ModalBody("Tempmessage", id='directoryprof_feedback_message'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Okay", id="directoryprof_closebtn", className="ms-auto", n_clicks=0
                    ),
                ),
            ],
            id="directoryprof_modal",
            is_open=False
        ),
    ],
    style = {'background-image': 'url("/assets/white bg.jpg")',
    'background-attachment': 'fixed',
    'background-repeat': 'repeat',
    'width': '100%',
    'position': 'absolute'}
)


@app.callback (
    [
        Output ('aoe_name', 'options'), 
        Output ('aoe_skills1', 'options'),
        Output ('aoe_skills2', 'options'),
        Output ('aoe_skills3', 'options'),
        Output ('directoryprof_toload', 'data'), 
        Output ('directoryprof_removerecord_div', 'style'), 
        Output ('skill_2div', 'style'),
        Output ('skill_3div', 'style')
    ],
    [
        Input('url', 'pathname'),   
        Input('aoe_name' ,'value'), 
        Input('aoe_skills1', 'value'),
        Input('aoe_skills2', 'value'),
        Input('aoe_skills3', 'value')
          
    ], 
    [
        State('url', 'search')
    ]
)

def directoryform_dropdown (pathname, aoe_value, skills_value1, skills_value2, skills_value3, search): 
    if pathname == '/directory/directory_profile': 
        if pathname == '/directory/directory_profile': 
            sql_aoe = """SELECT CONCAT(aoe_name, ' - ' , aoe_level) as label, aoe_id as value
            FROM aoe 
                INNER JOIN aoe_level al ON aoe.aoe_level_id = al.aoe_level_id 
            
            WHERE NOT aoe_delete_ind  
            """
            
            values_aoe = []
            cols_aoe = ['label', 'value']
            df_aoe = db.querydatafromdatabase(sql_aoe, values_aoe, cols_aoe)
            
            aoe_options = df_aoe.to_dict('records')
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            to_load = 1 if mode == 'edit' else 0
            removerecord_div = None if to_load else {'display':'none'}
            #print(aoe_value)
            
            
            
            sql_skill1 = """ SELECT skill_id, skill_name, aoe_id
            FROM skill

            WHERE NOT skill_delete_ind 
            """
            #print(aoe_value)
            values_skill1 = []
            cols_skill1 = ['skill_ID', 'skill_name', 'aoe_ID']
            df_skill1 = db.querydatafromdatabase(sql_skill1, values_skill1, cols_skill1)
            #print(df_skill1)
                
            skill_1 = df_skill1.to_dict ('records')
            #print(skill_1)
            skill_options1 = []
            skill_options2 = []
            skill_options3 = []
            
            for i in range(len(skill_1)): 
                if df_skill1['aoe_ID'][i] == aoe_value: 
                    skill_options1.append({'label': df_skill1['skill_name'][i], 'value': df_skill1['skill_ID'][i]})
                    if df_skill1['skill_ID'][i] != skills_value1: 
                        skill_options2.append({'label': df_skill1['skill_name'][i], 'value': df_skill1['skill_ID'][i]})
                        if df_skill1['skill_ID'][i] != skills_value2: 
                            skill_options3.append({'label': df_skill1['skill_name'][i], 'value': df_skill1['skill_ID'][i]})

            removeskill2 = {}
            removeskill3 = {}

            if (aoe_value != None):  
                removeskill2 = {'display':'inline'}
                removeskill3 = {'display':'inline'}
            else:
                skills_value1 = None
                skills_value2 = None
                skills_value3 = None
                removeskill2 = {'display':'none'}
                removeskill3 = {'display':'none'}
            
            if (skills_value1 != None): 
                removeskill2 = {'display':'inline'}
                removeskill3 = {'display':'inline'}
            else: 
                skills_value2 = None
                skills_value3 = None
                removeskill2 = {'display':'none'}
                removeskill3 = {'display':'none'}
                
            if skills_value2 != None: 
                removeskill3 = {'display':'inline'}
            else: 
                skills_value3 = None
                removeskill3 = {'display':'none'}
   
    else:
        raise PreventUpdate
    return [aoe_options, skill_options1,  skill_options2, skill_options3,  to_load, removerecord_div, removeskill2, removeskill3]

@app.callback (
    [
        Output('directoryprof_modal', 'is_open'), 
        Output('directoryprof_feedback_message', 'children'), 
        Output('directoryprof_closebtn', 'href'),
    ], 
    [
        Input('directoryprof_submitbtn', 'n_clicks'), 
        Input('directoryprof_closebtn', 'n_clicks')  
    ],
    [
        State('emp_name_last', 'value'),
        State('emp_name_first', 'value'),
        State('emp_name_middle', 'value'),
        State('emp_sex', 'value'),
        State('emp_bday', 'date'),
        State('emp_civil', 'value'),
        State('emp_degree', 'value'),
        State('emp_phone', 'value'),
        State('emp_email', 'value'),
        State('emp_address1', 'value'),
        State('emp_address2', 'value'),
        State('emp_address3', 'value'),
        State('emp_address4', 'value'),
        State('emp_postal', 'value'),
        State('aoe_name', 'value'), 
        State('aoe_skills1', 'value'),
        State('aoe_skills2', 'value'),
        State('aoe_skills3', 'value'),
        State('emp_hiredate', 'date'), 
        State('emp_sched', 'value'),
        State('emp_bank', 'value'),
        State('emp_bank_name', 'value'),
        State('emp_bank_num', 'value'), 
        State('url', 'search'),
        State('directoryprof_removerecord', 'value')     
    ]
)


def directoryprof_submit(submitbtn, closebtn, lastname, firstname, middlename, sex, bday, civil, degree, phone, email,
                         address1, address2, address3, address4, postal, aoe, skills1, skills2, skills3, hiredate, 
                         sched, bank, bankname, banknum, search, removerecord ):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        openmodal = False
        feedbackmessage = ' '
        okay_href = None
    else: 
        raise PreventUpdate
    
    if eventid == 'directoryprof_submitbtn' and submitbtn: 
        openmodal = True 
        inputs = [
            lastname, 
            firstname, 
            sex, 
            bday, 
            civil, 
            degree, 
            phone,
            email, 
            address1, 
            address2, 
            address3, 
            address4, 
            postal, 
            aoe, 
            skills1,
            hiredate, 
            sched, 
            bank, 
            bankname, 
            banknum
        ]
        
        # print (inputs)
        if not all (inputs): 
            feedbackmessage = "Please supply all information needed (at least one skill is needed)."
        # else save to db 
        else: 
            parsed = urlparse(search)
            mode = parse_qs(parsed.query)['mode'][0]
            
            if mode == "add": 
                
                sqlcode = """INSERT INTO emp(
                    emp_name_last, 
                    emp_name_first,
                    emp_name_middle,
                    emp_sex, 
                    emp_bday, 
                    emp_civil, 
                    emp_degree, 
                    emp_phone, 
                    emp_email, 
                    emp_address1,
                    emp_address2,
                    emp_address3,
                    emp_address4, 
                    emp_postal, 
                    aoe_id, 
                    skill_id_1, 
                    skill_id_2, 
                    skill_id_3, 
                    emp_hiredate, 
                    emp_sched, 
                    emp_bank, 
                    emp_bank_name, 
                    emp_bank_num, 
                    emp_delete_ind
                )
                VALUES (%s, %s,%s,%s, %s, %s,%s,%s, %s, %s,%s,%s, %s, %s,%s,%s, %s, %s,%s,%s, %s, %s,%s,%s)
                """
                
                values = [lastname, firstname, middlename, sex, bday, civil, degree, phone, email, address1, address2, address3, address4, postal, aoe, skills1, skills2, skills3, hiredate, sched, bank, bankname, banknum, False]
                db.modifydatabase(sqlcode, values)
                feedbackmessage = "Employee added to database"
                okay_href = '/directory'
            
            elif mode == 'edit': 
                parsed = urlparse(search)
                directoryid = parse_qs(parsed.query)['id'][0]
                
                
                sqlcode = """UPDATE emp
                SET
                    emp_name_last = %s, 
                    emp_name_first = %s,
                    emp_name_middle = %s,
                    emp_sex = %s, 
                    emp_bday = %s, 
                    emp_civil = %s, 
                    emp_degree = %s, 
                    emp_phone = %s, 
                    emp_email = %s, 
                    emp_address1 = %s,
                    emp_address2 = %s,
                    emp_address3 = %s,
                    emp_address4 = %s, 
                    emp_postal = %s, 
                    aoe_id = %s, 
                    skill_id_1 = %s, 
                    skill_id_2 = %s, 
                    skill_id_3 = %s, 
                    emp_hiredate = %s, 
                    emp_sched = %s, 
                    emp_bank = %s, 
                    emp_bank_name = %s, 
                    emp_bank_num = %s, 
                    emp_delete_ind = %s
                WHERE 
                    emp_id = %s
                """
                to_delete = bool(removerecord)
                values = [lastname, firstname, middlename, sex, bday, civil, degree, phone, email, address1, address2, address3, address4, postal, aoe, skills1, skills2, skills3, hiredate, sched, bank, bankname, banknum, to_delete, directoryid]
                db.modifydatabase(sqlcode, values)
                feedbackmessage = "Employee information changes are applied to the database"
                okay_href = '/directory'
            else: 
                raise PreventUpdate
    elif eventid == 'directoryprof_closebtn' and closebtn:
        pass
    else: 
        raise PreventUpdate
    return [openmodal, feedbackmessage, okay_href]

@app.callback (
    [
        Output('emp_name_last', 'value'),
        Output('emp_name_first', 'value'),
        Output('emp_name_middle', 'value'),
        Output('emp_sex', 'value'),
        Output('emp_bday', 'date'),
        Output('emp_civil', 'value'),
        Output('emp_degree', 'value'),
        Output('emp_phone', 'value'),
        Output('emp_email', 'value'),
        Output('emp_address1', 'value'),
        Output('emp_address2', 'value'),
        Output('emp_address3', 'value'),
        Output('emp_address4', 'value'),
        Output('emp_postal', 'value'),
        Output('aoe_name', 'value'), 
        Output('aoe_skills1', 'value'),
        Output('aoe_skills2', 'value'),
        Output('aoe_skills3', 'value'),
        Output('emp_hiredate', 'date'), 
        Output('emp_sched', 'value'),
        Output('emp_bank', 'value'),
        Output('emp_bank_name', 'value'),
        Output('emp_bank_num', 'value'), 
    ], 
    [
        Input('directoryprof_toload', 'modified_timestamp'), 
        Input('aoe_name', 'value'),
        Input('aoe_skills1', 'value'),
        Input('aoe_skills2', 'value'),
        Input('aoe_skills3', 'value')
    ], 
    [
        State('directoryprof_toload', 'data'), 
        State('url', 'search')
    ]
)

def loaddirectory (timestamp, aoevalue, skill_1, skill_2, skill_3, to_load, search): 
    if to_load == 1: 
        
        sql = """ SELECT emp_name_last, emp_name_first, emp_name_middle, emp_sex, emp_bday, emp_civil, emp_degree, emp_phone, emp_email, 
        emp_address1, emp_address2, emp_address3, emp_address4, emp_postal, aoe_id, skill_id_1, skill_id_2, skill_id_3, 
        emp_hiredate, emp_sched, emp_bank, emp_bank_name, emp_bank_num
        FROM emp 
        WHERE emp_id = %s  
        """
        parsed = urlparse(search)
        directoryid = parse_qs(parsed.query)['id'][0]
        
        val = [directoryid]
        colname = ['lastname', 'firstname', 'middlename', 'sex', 'bday', 'civil', 'degree', 'phone', 'email',
                   'address1', 'address2', 'address3', 'address4', 'postal', 'aoe', 'skill1', 'skill2', 'skill3', 
                   'hiredate', 'sched', 'bank', 'bankname', 'banknum']
        df = db.querydatafromdatabase (sql, val, colname)
        
        lastname = df['lastname'][0]
        firstname = df['firstname'][0]
        middlename = df['middlename'][0]
        sex = df['sex'][0]
        bday = df['bday'][0]
        civil = df['civil'][0]
        degree = df['degree'][0]
        phone = df['phone'][0]
        email = df['email'][0]
        address1 = df['address1'][0]
        address2 = df['address2'][0]
        address3 = df['address3'][0]
        address4 = df['address4'][0]
        postal = df['postal'][0]
        hiredate = df['hiredate'][0]
        sched = df['sched'][0]
        bank = df['bank'][0]
        bankname = df['bankname'][0]
        banknum = df['banknum'][0]
        
        aoe_database = df['aoe'][0]
        if aoevalue == None: 
            aoe = aoe_database
        else: 
            aoe = aoevalue 
        
        skill1_database = df['skill1'][0]
        if skill_1 == None: 
            skill1 = skill1_database
        else: 
            skill1 = skill_1
            
        skill2_database = df['skill2'][0]
        if skill_2 == None: 
            skill2 = skill2_database
        else: 
            skill2 = skill_2
            
        skill3_database = df['skill3'][0]
        if skill_3 == None: 
            skill3 = skill3_database
        else: 
            skill3 = skill_3
        
        
        return [lastname, firstname, middlename, sex, bday, civil, degree, phone, email, 
                address1, address2, address3, address4, postal, aoe, skill1, skill2, skill3, 
                hiredate, sched, bank, bankname, banknum]
    else: 
        raise PreventUpdate
        
 