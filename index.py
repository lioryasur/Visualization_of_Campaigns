import dash
from dash import Input, Output, State, html, dcc, dash_table, MATCH, ALL, ctx
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time, timedelta
import time as time_pck
import os
import dash_daq as daq
import requests
from html.parser import HTMLParser

from app import app
import pages

server = app.server

#app.enable_dev_tools( dev_tools_ui=True, dev_tools_serve_dev_bundles=True, debug=True)

# start = 23
# end = 15

# def in_between(now, start, end):
#     if start <= end:
#         return start <= now < end
#     elif datetime.today().weekday() > 4:
#         return True
#     else: # over midnight e.g., 23:30-04:15
#         return start <= now or now < end


def create_main_nav_link(icon, label, href):
    return dcc.Link(
        dmc.Group(
            direction='row',
            position='center',
            spacing=10,
            style={'margin-bottom':5},
            children=[
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),
                    size=25,
                    radius=5,
                    color='indigo',
                    variant="filled",
                    style={'margin-left':10}
                ),
                dmc.Text(label, size="sm", color="gray", style={'font-family':'IntegralCF-Regular'}),
            ]
        ),
        href=href,
        style={"textDecoration": "none"},
    )

def create_accordianitem(icon, label, href):
    return dcc.Link(
        dmc.Group(
            direction='row',
            position='left',
            spacing=10,
            style={'margin-bottom':10},
            children=[
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),
                    size=30,
                    radius=30,
                    color='indigo',
                    variant="light",
                ),
                dmc.Text(label, size="sm", color="gray", style={'font-family':'IntegralCF-Regular'}),
            ]
        ),
        href=href,
        style={"textDecoration": "none"},
    )

app.layout = dmc.MantineProvider(
    id = 'dark-moder', 
    withGlobalStyles=True, 
    children = [
        html.Div(
            children = [

                # dcc.Interval(
                #     id='interval',
                #     n_intervals=0,
                #     interval=10*1000,
                # ),

                # html.Div(
                #     id = 'timer-sales-holder',
                #     style = {'display':'None'}
                # ),


                # dcc.Interval(
                #     id='minute-int',
                #     n_intervals=0,
                #     interval=2*1000,
                # ),

                dmc.Header(
                    height=70,
                    fixed=True,
                    pl=0,
                    pr=0,
                    pt=0,
                    style = {'background-color':'skyblue', 'color':'whitesmoke'},
                    children=[

                        # dmc.Container(
                        #     fluid=True,
                        #     pt=0,
                        #     pl=0,
                        #     pr=0,
                        #     children=[
                        #         dmc.Group(
                        #             id = 'style-1',
                        #             spacing=0,
                        #             position="left",
                        #             align="flex-start",
                        #             noWrap=True,
                        #             style={'overflow-x':'scroll', 'overflow-y':'hidden'},
                        #             children=[

                        #                 #])

                        #             ]
                        #         ),
                        #     ]
                        # ),

                        dmc.Container(
                            fluid=True,
                            children=[
                                dmc.Group(
                                    position="apart",
                                    align="center",
                                    children=[
                                        dmc.Center(
                                            children=[
                                                dcc.Link(
                                                    dmc.ThemeIcon(
                                                        html.Img(src= '..\\assets\\ibm_logo.png', style={'width':43}),
                                                        radius='sm',
                                                        size=44,
                                                        variant="filled",
                                                        color="blue",
                                                    ),
                                                    href=app.get_relative_path("/"),
                                                ),
                                                dcc.Link(
                                                    href=app.get_relative_path("/"),
                                                    style={"paddingTop": 2, "paddingLeft":10, "paddingBottom":5, "paddingRight":10, "textDecoration": "none"},
                                                    children=[
                                                        dmc.MediaQuery(
                                                            smallerThan="sm",
                                                            styles={"display": "none"},
                                                            children=[
                                                                dmc.Group(direction='column', align='center', spacing=0, position='center', children=[
                                                                    dmc.Text("Plotly Dash", size="lg", color="gray", style={'font-family':'IntegralCF-ExtraBold'}),
                                                                    dmc.Badge("2022 Holiday Challenge", variant="outline", color="blue", size="sm",  style={'margin-top':4})]
                                                                ) #leftSection=[html.Img(src='https://plotly.chiefs.work/ticketing/assets/Teams/NFL.svg',
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                dmc.MediaQuery(
                                                    largerThan="sm",
                                                    styles={"display": "none"},
                                                    children=[
                                                        dmc.Group(direction='column', align='flex-start', spacing=0, position='center', 
                                                            children=[
                                                                dmc.Text("Plotly Dash", size="sm", color="gray", style={'font-family':'IntegralCF-ExtraBold'}),
                                                                dmc.Badge("2022 Holiday Challenge", variant="outline", color="red", size="xs")
                                                            ]
                                                        )
                                                    ]
                                                ),
                                            ]
                                        ),
                                        dmc.Group(
                                            direction = 'row',
                                            position="right",
                                            align="center",
                                            spacing="md",
                                            children=[
                                                html.Div(id = 'indicatorbox', className = 'indicator-box',
                                                    children=[
                                                        html.Div(id = 'indicatorpulse', className='indicator-pulse', children=[]),
                                                        html.Span(id = 'liveindicator', className= 'live-indicator', children=['LIVE']),
                                                        
                                                    ]
                                                ),
                                                html.A(
                                                    dmc.ThemeIcon(
                                                        DashIconify(icon = 'mdi:linkedin')
                                                    ),
                                                    href = 'https://www.linkedin.com/in/andrewschutte/',
                                                    target ='_blank'
                                                ),
                                                
                                                html.A(
                                                   dmc.ThemeIcon(
                                                        DashIconify(icon = 'mdi:twitter')
                                                    ), 
                                                    href = 'https://twitter.com/Andrewschutte2',
                                                    target ='_blank'
                                                ),

                                                html.A(
                                                    dmc.ThemeIcon(
                                                        DashIconify(icon = 'mdi:github'),
                                                        color = 'dark'
                                                    ),
                                                    href = 'https://github.com/almostBurtMacklin/Plotly-Challenge',
                                                    target ='_blank'
                                                )
                                            ],
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
                dmc.Modal(
                    id = 'the-modal',
                    overflow = 'inside',
                    size = 'xl',
                    children = [
                        
                    ],
                    opened = False
                ),

                dmc.Navbar(
                    fixed=True,
                    width={"base": 300},
                    pl='sm',
                    pr='xs',
                    pt=0,
                    hidden=True,
                    hiddenBreakpoint='sm',
                    children=[
                        dmc.ScrollArea(
                            offsetScrollbars=True,
                            type="scroll",
                            children=[
                                dmc.Group(
                                    direction = 'column',
                                    align = 'center',
                                    position = 'center',\
                                    spacing = 'xs',
                                    children =[
                                        dmc.Text('Built By: Andrew Schutte', style = {'font-family':'IntegralCF-RegularOblique'}, size = 'sm'),
                                        dmc.Text('Kansas City, USA', style = {'font-family':'IntegralCF-RegularOblique'}, size = 'sm')
                                    ]
                                ),
                                
                                #html.Img(src='https://plotly.chiefs.work/ticketing/assets/SA.svg', id  = 'sa-logo', style={'width':160, 'margin-left':50}),
                                dmc.Divider(label='Customer Exploration', style={"marginBottom": 20, "marginTop": 5}),
                                dmc.Group(
                                    direction="column",
                                    children=[
                                        create_main_nav_link(
                                            icon="mdi:people-group",
                                            label="Customer Base",
                                            href=app.get_relative_path("/"),
                                        ),
                                        create_main_nav_link(
                                            icon="mdi:magnify",
                                            label="Churn Investigation",
                                            href=app.get_relative_path("/churn"),
                                        ),
                                        create_main_nav_link(
                                            icon="ooui:text-summary-ltr",
                                            label="Churn Prediction",
                                            href=app.get_relative_path("/summary"),
                                        ),
                                    ],
                                ),
                                # dmc.Divider(label='Ticket Sales', style={"marginBottom": 15, "marginTop": 10}),

                                # dmc.Group(
                                #     direction="column",
                                #     children=[
                                #         create_main_nav_link(
                                #             icon="mdi:people-group",
                                #             label="Single Game Sales",
                                #             href=app.get_relative_path("/singlegame-sales"),
                                #         ),

                                #         create_main_nav_link(
                                #             icon="bi:people",
                                #             label="New Season Ticket Sales",
                                #             href=app.get_relative_path("/newstm-sales"),
                                #         ),

                                #         create_main_nav_link(
                                #             icon="fa:refresh",
                                #             label="Renewal",
                                #             href=app.get_relative_path("/renewal"),
                                #         ),
                                #         create_main_nav_link(
                                #             icon="material-symbols:sports-football-rounded",
                                #             label="Playoffs",
                                #             href=app.get_relative_path("/playoff_tickets"),
                                #         ),
                                #     ]
                                # ),

                                # dmc.Divider(style={"marginBottom": 0, "marginTop": 10}),

                                # dmc.Accordion(
                                #     #iconPosition='right',
                                #     multiple=True,
                                #     style={'font-family':'IntegralCF-Regular'},
                                #     children=[
                                #         dmc.AccordionItem(
                                #             icon=[DashIconify(icon='bi:people', width=18)],
                                #             label="Sales Rep Tracking",
                                #             children=[
                                #                 create_accordianitem(
                                #                     icon="iconoir:leaderboard-star",
                                #                     label="Sales Leaderboard",
                                #                     href=app.get_relative_path("/salesrep-leaderboard"),
                                #                 ),
                                #                 create_accordianitem(
                                #                     icon="iconoir:leaderboard-star",
                                #                     label="Deposit Leaderboard",
                                #                     href=app.get_relative_path("/salesrep-deposits"),
                                #                 ),
                                #             ]
                                #         ),
                                #         dmc.AccordionItem(
                                #             icon=[DashIconify(icon='bx:party', width=18)],
                                #             label="Season Ticket Member Events",
                                #             children=[

                                #                 create_accordianitem(
                                #                     icon="fa:refresh",
                                #                     label="Draft Fest",
                                #                     href=app.get_relative_path("/stmevents-draftfest"),
                                #                 ),

                                #                 create_accordianitem(
                                #                     icon="fluent:tent-16-filled",
                                #                     label="Training Camp",
                                #                     href=app.get_relative_path("/stmevents-training-camp"),
                                #                 ),

                                #             ]
                                #         ),
                                #         dmc.AccordionItem(
                                #             icon=[DashIconify(icon='bi:file-earmark-bar-graph', width=18)],
                                #             label="Reporting",
                                #             children=[
                                #                 create_accordianitem(
                                #                     icon="fa:refresh",
                                #                     label="Box Office",
                                #                     href=app.get_relative_path("/reporting-boxoffice"),
                                #                 ),
                                #             ]
                                #         ),
                                #     ],
                                # ),
                            ],
                        )
                    ],
                ),

                dcc.Location(id='url'),
                dmc.MediaQuery(
                    largerThan="xs",
                    styles={'height':'100%', 'margin-left':'300px', 'margin-top':70},
                    children = [
                        html.Div(
                            id='content',
                            style={'margin-top':'70px'}
                        )
                    ],
                ),
            ]
        )
    ]
)

#analytics = dash_user_analytics.DashUserAnalytics(app, automatic_routing=False)

@app.callback(Output('content', 'children'),
                [Input('url', 'pathname')])
def display_content(pathname):
    page_name = app.strip_relative_path(pathname)
    if not page_name:  # None or ''
        return pages.customerbase.layout
    elif page_name == 'churn':
        return pages.churn.layout
    elif page_name == 'summary':
        return pages.summary.layout

@app.callback([Output(component_id='liveindicator', component_property='className'),
              Output(component_id='indicatorpulse', component_property='className')],
             [Input(component_id='interval', component_property='n_intervals')])

def update_indicator(n):

    # if (os.path.getmtime('/data/live_sales_22.feather') - time_pck.time()) < -60:
    #     return 'live-indicator-off', 'indicator-pulse-off'
    # else:
    return 'live-indicator', 'indicator-pulse'




if __name__ == '__main__':

    app.run_server(debug=True)
