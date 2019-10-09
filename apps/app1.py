import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app import app

""" Load data """
df = pd.read_csv(r"data/company_profiles.csv")
df.dropna(inplace=True)
dff = df[["price", "industry", "name"]].groupby("industry").agg(
    {"price": "mean", "name": "count"}).rename(
    columns={"price": "price_avg", "name": "count"})
dff = dff.round(2)

list_of_industries = df["industry"].unique().tolist()

""" STYLING """

COLORS = {
    'background': '#556B2F',
    'text': '#FFFFF0',
    'border': '#BCEE68',
    'darktext': '#050505'
}
MY_COLS = {
    "blue": "#00688B",
    "grey": "#9E9E9E"}

""" Layout """

layout = html.Div([
    html.Div([

        html.Div([
            html.Div([html.H6("Share price distribution by industry")], style={"textAlign": "center"}),
            dcc.Graph(
                id='crossfilter-scatter',
                figure={
                    'data': [go.Scatter(
                        x=dff["price_avg"],
                        y=dff["count"],
                        text=[i for i in dff.index],
                        customdata=dff.index,
                        mode='markers',
                        marker={
                            'size': 15,
                            'color': MY_COLS["blue"],
                            'opacity': 0.5,
                            'line': {'width': 0.5, 'color': 'white'}})],
                    'layout': go.Layout(
                        xaxis={'automargin': True,
                               'title': "average share price"},
                        yaxis={'automargin': True,
                               'title': "number of companies"},
                        margin={'l': 30, 'b': 10, 't': 10, 'r': 10},
                        height=420,
                        hovermode='closest')},
                hoverData={'points': [{'customdata': 'Homebuilding & Construction',
                                       'text': 'Homebuilding & Construction'}]})],
            style={'width': '40%', 'height': '30%', 'padding': '0 20', 'display': 'inline-block'}),

        html.Div([
            dcc.Markdown([""" 
        ### text
        bla bla
        >bla 

        >bla 

        >bla

        >bla

        >bla

        *header*

        """], style={"textAlign": "center",
                     'width': '70%', 'float': 'right',
                     'display': 'inline-block', 'backgroundColor': MY_COLS["blue"]}),
            html.Div([
                html.H6("Text title")],
                style={"textAlign": "center", 'backgroundColor': MY_COLS["blue"]}),

            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id="dropdown_industry",
                        options=[{'label': str(i), 'value': i} for i in list_of_industries],
                        value="Asset Management"
                    )], style={"width": "40%",
                               'color': COLORS["darktext"],
                               'margin': '5px'}),

                html.Div([
                    dcc.Link('Navigate to Industry Analysis', href='/apps/app2',
                             style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                    'color': 'white', 'padding': '5px 10px 100px'}),
                ])
            ],
                style={'backgroundColor': MY_COLS["blue"],
                       'padding': '2px 5px', 'color': COLORS["text"]})
        ],
            style={'width': '60%', 'float': 'right',
                   'display': 'inline-block', 'backgroundColor': MY_COLS["blue"]})],

        style={'color': COLORS["darktext"]}),

    html.Div([
        dcc.Graph(id="my-boxplot")],
        style={"width": "100%", "height": "30%", 'padding': '2px 5px'})])


@app.callback(
    Output('my-boxplot', 'figure'),
    [Input('crossfilter-scatter', 'hoverData')])
def update_figure(hoverOn):
    traces = []
    for industry in list_of_industries:
        if industry == hoverOn["points"][0]["customdata"]:
            traces.append(go.Box(y=df[df["industry"] == industry]["price"],
                                 name=industry, marker={"size": 4, "color": MY_COLS["blue"], }))
        else:
            traces.append(go.Box(y=df[df["industry"] == industry]["price"],
                                 name=industry, marker={"size": 4, "color": MY_COLS["grey"], }))
    return {"data": traces,
            "layout": go.Layout(autosize=True,
                                margin={"l": 50, "b": 200, "r": 20, "t": 10},
                                xaxis={"showticklabels": True},
                                yaxis={"title": "Share price distribution", "range": [-10, 300]},
                                showlegend=False)}
