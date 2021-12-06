#<--------------------NAME: RAHUL MISHRA----------ROLL NO.: 102083033----------GROUP: 3COE7-------------------->

#<----------INSTALLING DEPENDENCIES---------->
# pip install dash
# pip install plotly
# pip install pandas

#<----------IMPORTING DEPENDENCIES---------->
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input

#<----------READING DATA FROM CSV FILE---------->
data=pd.read_csv("WCT20.csv")

#<----------ADDING EXTERNAL STYLESHEET FOR FONT---------->
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

#<----------CREATING INSTANCE OF DASH CLASS---------->
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#<----------DEFINING TITLE OF THE DASH WEBSITE---------->
app.title = "ICC T-20 World Cup 2021"

#<----------DEFINING LAYOUT OF THE DASH APPLICATION---------->
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🏏", className="header-emoji"),
                html.H1(
                    children="ICC T-20 World Cup Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the toss preferences of different teams and affect of venues on the target achieved in T-20 World Cup held in 2021",
                    className="header-description",
                ),
                html.P(
                    children="By Rahul Mishra (102083033)", className="intro"     #MY NAME & ROLL NO. 
                ),
                html.Br(),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Venue", className="menu-title"),     #Dropdown menu to choose VENUE
                        dcc.Dropdown(
                            id="venue-filter",
                            options=[
                                {"label": venue, "value": venue}
                                for venue in np.sort(data.venue.unique())
                            ],
                            value="Abu_Dhabi",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Time", className="menu-title"),     #Dropdown menu to choose TIME of play of match
                        dcc.Dropdown(
                            id="time-filter",
                            options=[
                                {"label": scheduled_time, "value": scheduled_time}
                                for scheduled_time in data.time.unique()
                            ],
                            value="afternoon",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(children="Graph Type", className="menu-title"),     #Dropdown menu to choose GRAPH TYPE
                        dcc.Dropdown(
                            id="graph-filter",
                            options=[
                                {"label": graph_choice, "value": graph_choice}
                                for graph_choice in ["Line Graph", "Bar Graph"]
                            ],
                            value="Line Graph",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                ],
            className="menu",
        ),
        html.Br(),
        html.Div(     #Defining layout for the Graph depicting TARGET achieved
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="target-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Hr(),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Team", className="menu-title"),     #Dropdown menu to choose TEAM name 
                        dcc.Dropdown(
                            id="team-filter",
                            options=[
                                {"label": team, "value": team}
                                for team in np.sort(data.Winner_toss.unique())
                            ],
                            value="Afghanistan",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                ],
            className="menu",
        ),  
        html.Br(),
        html.Div(     #Defining layout for the Graph depicting TOSS PREFERENCE of selected team
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="toss-chart", config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

#<----------CALLBACK FUNCTION TO MAKE THE APPLICATION REACT TO USER INTERACTIONS---------->
@app.callback(
    [Output("target-chart", "figure"),Output("toss-chart", "figure")],
    [
        Input("graph-filter", "value"),
        Input("venue-filter", "value"),
        Input("time-filter", "value"),
        Input("team-filter", "value"),
    ],
)

#<----------FUNCTION DEFINATION TO UPDATE GRAPHS AS PER USER CHOICE---------->
def update_charts(graph_choice,venue, scheduled_time,team):

    #<----------GRAPH 1---------->
    if(graph_choice == "Line Graph"):     #When chosen graph type is LINE GRAPH
        mask = (
        (data.venue == venue)
        & (data.time == scheduled_time)
        )
    
        filtered_data = data.loc[mask, :]
    
        target_chart_figure = {
        
        "data": [
            {
                "x": filtered_data["Match_No"],
                "y": filtered_data["target"],
                "type": "lines",
                "hovertemplate": "runs%{y:}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Target at different venues at different time schedules",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"], 
        },
    }
    else:          #When chosen graph type is BAR GRAPH
        mask = (
        (data.venue == venue)
        & (data.time == scheduled_time)
        )
    
        filtered_data = data.loc[mask, :]
    
        target_chart_figure = {
        
        "data": [
            {
                "x": filtered_data["Match_No"],
                "y": filtered_data["target"],
                "type": "bar",
                "hovertemplate": "runs%{y:}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Target at different venues at different time schedules",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"], 
        },
    }

    #<----------GRAPH 2---------->
    mask2 = (
        ( data.Winner_toss == team)
    )
    filtered_data2 = data.loc[mask2, :]
    toss_chart_figure = {
        "data": [
            {
                "x": filtered_data2["Match_No"],
                "y": filtered_data2["Toss_descision"],
                "type": "line",
                #"hovertemplate": "runs%{y:}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Toss preferences for different teams",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"], 
        },
    }
    return target_chart_figure, toss_chart_figure

#<----------TO RUN DASH APPLICATION ON LOCAL HOST---------->
if __name__ == "__main__":
    app.run_server(debug=True)