import plotly.graph_objs as go
import pandas as pd

""" General load and merge to full dataset"""

YEARS = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
cp = pd.read_csv(r"data/company_profiles.csv")

def load_df(YEARS):
    df_is = pd.read_csv(r"data/df_is_full.csv")
    df_bs = pd.read_csv(r"data/df_bs_full.csv")
    df_m = pd.read_csv(r"data/df_metrics_full.csv")
    df_is["type"] = "income statement"
    df_bs["type"] = "balance sheet"
    df_m["type"] = "metrics"
    df = pd.concat([df_is, df_bs, df_m], axis=0).reset_index()
    df.dropna(inplace=True)
    for yr in YEARS:
        df[str(yr)] = df[str(yr)].round(2)
    return df


df = load_df(YEARS)

""" INDUSTRY APP"""
""" scatter DF """


def df_for_industry_scatter(df, industry, x_value, y_value, range_slider_value):
    dff = df[df.industry == industry]
    dfff = dff[(dff.line_item == x_value) | (dff.line_item == y_value)]
    dfff = pd.pivot_table(pd.melt(dfff, id_vars=["symbol", "line_item"],
                                  value_vars=["2009", "2010", "2011", "2012",
                                              "2013", "2014", "2015", "2016",
                                              "2017", "2018"]),
                          index=["symbol", "variable"],
                          columns="line_item",
                          values="value", fill_value=0).reset_index()
    dfff = dfff.rename(columns={"variable": "year"})
    dfff["year"] = dfff["year"].astype(int)
    dfff = dfff[dfff.year.between(range_slider_value[0],
                                       range_slider_value[1], inclusive=True)]
    return dfff


""" plot DF """


def df_for_industry_plot(df, symbol, axis, industry):
    dff = df[df.industry == industry]
    dfff = dff[dff.line_item == axis]
    dfff = pd.pivot_table(pd.melt(dfff, id_vars=["symbol", "line_item"],
                                  value_vars=["2009", "2010", "2011", "2012",
                                              "2013", "2014", "2015", "2016",
                                              "2017", "2018"]),
                          index=["symbol", "variable"],
                          columns="line_item", values="value", fill_value=0).reset_index()
    dfff = dfff.rename(columns={"variable": "year"})
    dfff["year"] = dfff["year"].astype(int)
    dfff_line = dfff[dfff.symbol == symbol]
    dfff_mkt = dfff.groupby(["year"], as_index=False).mean()
    return dfff_line, dfff_mkt


""" create PLOT """


def create_time_series(dff, dff_mkt, title: str, line_item):
    traces = []
    # company data
    traces.append(go.Scatter(
            x=dff.iloc[:, 1],
            y=dff.loc[:, line_item],
            name="company actual",
            mode='lines+markers'
        ))

    traces.append(go.Scatter(
        x=dff_mkt.iloc[:, 0],
        y=dff_mkt.loc[:, line_item],
        name="industry average",
        mode='lines+markers'
    ))

    return {"data": traces,
            'layout': {'height': 225,
            'margin': {'l': 40, 'b': 30, 'r': 10, 't': 40},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title, 'font': {'size': 14, 'color': "black"},
                'bordercolor': 'black', 'borderwidth':2,
                'borderpad': 4, 'bgcolor': 'white',
                'opacity': 0.5
            }],
            'xaxis': {'showgrid': False},
            'yaxis': {'automargin': True}}}


""" create scatter """


def create_scatter(dfff, x_value, y_value, COMP_NAME, COLORS):
    return {
        'data': [go.Scatter(
            x=dfff[x_value],
            y=dfff[y_value],
            text=["<br>".join([dfff.iloc[i]["symbol"],
                               COMP_NAME[dfff.iloc[i]["symbol"]],
                              str(dfff.iloc[i]["year"])]
                              ) for i in range(len(dfff))],

            customdata=dfff["symbol"],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            title={'text': "Financial indicators by company", 'font': {
                'family': "Open Sans",
                'size': 18,
                'color': COLORS["darktext"]}},
            xaxis={'automargin': True,
                'title': x_value
            },
            yaxis={'automargin': True,
                'title': y_value
            },
            margin={'l': 60, 'b': 50, 't': 50, 'r': 20},
            height=420,
            hovermode='closest'
        )
    }


""" DATATABLE UDFs """


""" Create df for DataTable """


def df_for_datatable(df, cp):
    df_dt = pd.pivot_table(data=df,
                           index=["symbol", "industry"],
                           columns="line_item",
                           values="2018",
                           fill_value=0).reset_index()
    df_dt = pd.merge(cp[["name", "symbol"]], df_dt,
                     left_on="symbol",
                     right_on="symbol")
    df_dt = df_dt.sort_values(by="industry")
    return df_dt


"""" Create Barplots for DataTable """

COLORS = ["#00688B", "#FF6A6A", "#A2B5CD"]
def create_barplot_pl(df):
    # define figure

    # Plot 1 -> PL
    cols_pl = ['Revenue', 'Gross Profit', 'Operating Income', 'EBIT', 'EBITDA',
               'Cost of Revenue', 'Interest Expense', 'Operating Expenses',
               'R&D Expenses', 'Net Income']

    cols_choice = []
    for c in df.columns:
        if c in cols_pl:
            cols_choice.append(c)
    # add traces for each company
    traces = []
    for row in range(df.shape[0]):
        traces.append(go.Bar(
            x=cols_choice,
            y=df.iloc[row][cols_choice].values,
            name=df.iloc[row]["symbol"],
            marker_color=COLORS[row]
        ))

    return {"data": traces,
            'layout': dict(title='P&L Metrics',
                        barmode='group',
                        xaxis_tickangle=-45,
                        bargap=0.15,
                        bargroupgap=0.1,
                        margin={'l': 30, 'b': 140, 't': 30, 'r': 10},
                        height= '400px',
                        width=400
                      )}


def create_barplot_bs(df):

    # Plot 2 -> BS
    cols_bs = ['Cash and cash equivalents', 'Long-term debt', 'Net Debt',
               'Short-term debt', 'Total assets',
               'Total current assets', 'Total current liabilities', 'Total debt',
               'Total liabilities', 'Total non-current assets',
               'Total non-current liabilities', 'Total shareholders equity',
               'Working Capital', 'Average Inventory', 'Average Payables',
                'Average Receivables']

    cols_choice_bs = []
    for c in df.columns:
        if c in cols_bs:
            cols_choice_bs.append(c)
    # add traces for each company
    traces = []
    for row in range(df.shape[0]):
        traces.append(go.Bar(
            x=cols_choice_bs,
            y=df.iloc[row][cols_choice_bs].values,
            name=df.iloc[row]["symbol"],
            marker_color=COLORS[row]
        ))

    return {"data": traces,
            'layout': dict(title='B&S Metrics',
                           barmode='group',
                           xaxis_tickangle=-45,
                           bargap=0.15,
                           bargroupgap=0.1,
                           margin={'l': 30, 'b': 140, 't': 30, 'r': 10},
                           height='400px',
                           width=500
                           )}


def create_barplot_ps(df):

    # Plot 3 -> Metrics
    cols_ps = ['Revenue per Share', 'Net Income per Share',
              'Operating Cash Flow per Share',
              'Cash per Share', 'Dividend per Share',
              'Interest Debt per Share', 'Interest Coverage', 'PE ratio',
               'PB ratio']

    cols_choice_ps = []
    for c in df.columns:
        if c in cols_ps:
            cols_choice_ps.append(c)
    # add traces for each company
    traces = []
    for row in range(df.shape[0]):
        traces.append(go.Bar(
            x=cols_choice_ps,
            y=df.iloc[row][cols_choice_ps].values,
            name=df.iloc[row]["symbol"],
            marker_color=COLORS[row]
        ))

    return {"data": traces,
            'layout': dict(title='Values per share/ ratios',
                           barmode='group',
                           xaxis_tickangle=-45,
                           bargap=0.15,
                           bargroupgap=0.1,
                           margin={'l': 30, 'b': 140, 't': 30, 'r': 10},
                           height='500px',
                           width=350
                           )}


def create_barplot_m(df):

    # Plot 3 -> Metrics
    cols_m = ['Current ratio', 'Dividend Yield',
              'Profit Margin', 'Gross Margin',
              'EPS', 'ROE', 'ROIC',
              'Debt to Assets', 'Debt to Equity',
              'Net Debt to EBITDA']

    cols_choice_m = []
    for c in df.columns:
        if c in cols_m:
            cols_choice_m.append(c)
    # add traces for each company
    traces = []
    for row in range(df.shape[0]):
        traces.append(go.Bar(
            x=cols_choice_m,
            y=df.iloc[row][cols_choice_m].values,
            name=df.iloc[row]["symbol"],
            marker_color=COLORS[row]
        ))

    return {"data": traces,
            'layout': dict(title='Other Metrics',
                           barmode='group',
                           xaxis_tickangle=-10,
                           bargap=0.15,
                           bargroupgap=0.1,
                           margin={'l': 30, 'b': 140, 't': 30, 'r': 10},
                           height='400px',
                           width=350
                           )}
