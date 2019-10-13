import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
import udf


""" Data """
df_dt = udf.df_for_datatable(udf.df, udf.cp)

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
    dcc.Markdown([""" 
            ## Year 2018 - Financial Information by company 
            *Choose up to 3 companies to compare the financial information, and financial metrics/ ratios*
            """], style={"textAlign": "center",
               'backgroundColor': MY_COLS["blue"],
               'color': 'white'
               }),
    html.Div([
            dcc.Link('Navigate back home', href='/',
                         style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                                'padding': '0px 0px 0px 0px', 'color': 'red'}),
            html.Br(),
            dcc.Link('Navigate to Industry Analysis', href='/apps/industryApp',
                     style={'font-family': 'Times New Roman, Times, serif', 'font-weight': 'bold',
                            'color': 'white'})
        ])], style={'backgroundColor': MY_COLS["blue"]
               }),

    dash_table.DataTable(
        id='datatable_interact',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False} for i in df_dt.columns
        ],
        style_table={'overflowX': 'scroll',
                     'maxHeight': '300px',
                     'overflowY': 'scroll'
                     },
        style_cell={
                'minHeight': '10px', 'maxHeight': '180px',
                'minWidth': '0px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            },
        data=df_dt.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        fixed_rows={'headers': True},
        column_selectable=False,
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[0, 1]
    ),
    html.Div([
    html.Div([dcc.Graph(id='bar_plot')], style={'display': 'inline-block'}),
    html.Div([dcc.Graph(id='bar_plot1')], style={'display': 'inline-block'}),
    html.Div([dcc.Graph(id='bar_plot2')], style={'display': 'inline-block'}),
    html.Div([dcc.Graph(id='bar_plot3')], style={'display': 'inline-block'})
], style={'display': 'inline-block'})
])



@app.callback(
    [Output('bar_plot', "figure"),
     Output('bar_plot1', "figure"),
     Output('bar_plot2', "figure"),
     Output('bar_plot3', "figure")],
    [Input('datatable_interact', "selected_rows")])
def update_graphs(selected_rows):
    dff = df_dt
    # if none cols selected show all
    # limit rows to max 3
    if selected_rows is not None:
        rows_range = selected_rows[-3:]
        dff = dff[dff.index.isin(rows_range)]
        return udf.create_barplot_pl(dff), udf.create_barplot_bs(dff), udf.create_barplot_ps(dff), \
               udf.create_barplot_m(dff)
    else:
        return None, None, None, None

