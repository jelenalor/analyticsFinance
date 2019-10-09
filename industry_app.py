import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2


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
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)