import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app import app
# from apps import app1, app2

""" Load data """
df = pd.read_csv(r"data/company_profiles.csv")
df.dropna(inplace=True)
dff = df[["price", "industry", "name"]].groupby("industry").agg(
    {"price": "mean", "name": "count"}).rename(
    columns={"price": "price_avg", "name": "count"})
dff = dff.round(2)

list_of_industries = df["industry"].unique()

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

app.layout = html.Div([
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
        style={'width': '30%', 'height': '20%', 'padding': '0 20', 'display': 'inline-block'}),

    html.Div([html.Div([
        html.H6("Text title")],
        style={"textAlign": "center"}),
        html.Div([""" 
    text
    bla bla
    """], style={"textAlign": "center",
                 'width': '70%', 'float': 'right', 'display': 'inline-block'})],
        style={'width': '70%', 'float': 'right', 'display': 'inline-block'})],
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
                                 name=industry, marker={"size": 4, "color": MY_COLS["blue"],}))
        else:
            traces.append(go.Box(y=df[df["industry"] == industry]["price"],
                                 name=industry, marker={"size": 4, "color": MY_COLS["grey"],}))
    return {"data": traces,
            "layout": go.Layout(autosize=True,
                                margin={"l": 50, "b": 200, "r": 20, "t": 10},
                                xaxis={"showticklabels": True},
                                yaxis={"title": "Share price distribution", "range": [-10, 300]},
                                showlegend=False)}


# layout_index = html.Div([
#     dcc.Link('Navigate to "/apps/app1"', href='/apps/app1'),
#     html.Br()
# ])
#
#
# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/apps/app1':
#         return app1.layout
#     elif pathname == '/apps/app2':
#         return app2.layout
#     else:
#         return '404'


if __name__ == '__main__':
    app.run_server(debug=True)