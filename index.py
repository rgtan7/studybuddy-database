from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import webbrowser
from app import app
from apps import commonmodules as cm
from apps import home, login, directory, skills, aoe, equipment, aoepage, skillspage, skills_form
from apps import directory_profile, signup, equipment_profile


CONTENT_STYLE = {
    "margin-top": "1em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

server = app.server
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),
        dcc.Store(id='sessionlogout', data=False, storage_type='session'),
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        dcc.Store(id='currentrole', data=-1, storage_type='session'),
        html.Div(cm.navbar,id ='navbar_div'), 
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)
@app.callback(
    [
        Output('page-content', 'children'),
        Output('navbar_div', 'style'),
        Output('sessionlogout', 'data'),
    ],
    [
        Input('url', 'pathname')
    ], 
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
    ]
)
def displaypage (pathname, sessionlogout, currentuserid):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0] 
    else:
        raise PreventUpdate
    if eventid == 'url':
        if currentuserid < 0:
            sessionlogout = True
            if pathname in ['/', '/login']:
                returnlayout = login.layout
            elif pathname == '/signup':
                returnlayout = signup.layout
            else:
                returnlayout = '404: request not found'
        else: 
            
            currentuserid_dummy = currentuserid 
            sessionlogout = False

            if pathname == '/logout':
                returnlayout = login.layout
                sessionlogout = True

            elif pathname == '/home':
                returnlayout = home.layout

            elif pathname == '/directory':
                returnlayout = directory.layout
                
            elif pathname == '/directory/directory_profile':
                returnlayout = directory_profile.layout

            elif pathname == '/skills':
                returnlayout = skills.layout
                
            elif pathname == '/skills_page': 
                returnlayout = skillspage.layout
            
            elif pathname == '/skills_form': 
                returnlayout = skills_form.layout

            elif pathname == '/aoe':
                returnlayout = aoe.layout
            
            elif pathname == '/aoe/aoe_profile':
                returnlayout = aoepage.layout 
                
            elif pathname == '/equipment':
                returnlayout = equipment.layout
            
            elif pathname == '/equipment/equipment_profile':
                returnlayout = equipment_profile.layout
            
            else:
                returnlayout = "404: request not found"
    else:
        raise PreventUpdate
    
    navbar_div = {'display':  'none' if sessionlogout else 'unset'}
    return [returnlayout, navbar_div, sessionlogout]



if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)
