import pandas as pd


""" get company profiles """
""" this was previously scraped by myself """

# Drop na for clean dataset
comp_prof = pd.read_csv(r"data/company_profiles.csv")
comp_prof.dropna(inplace=True)

index_keep = ['Average Inventory', 'Average Payables', 'Average Receivables', 'Cash per Share',
       'Current ratio', 'Days Payables Outstanding', 'Days Sales Outstanding',
       'Days of Inventory on Hand', 'Debt to Assets', 'Debt to Equity',
       'Dividend Yield', 'Interest Coverage', 'Interest Debt per Share', 'Inventory Turnover',
        'Net Debt to EBITDA', 'Net Income per Share', 'Operating Cash Flow per Share', 'PB ratio',
       'PE ratio', 'Payables Turnover', 'ROE', 'ROIC', 'Receivables Turnover', 'Revenue per Share',
       'Shareholders Equity per Share', 'Working Capital']

list_of_industry = comp_prof["industry"].unique()

df = pd.DataFrame()
industries_processed = []
for industry in list_of_industry:
    list_of_tickers = comp_prof[comp_prof.industry == industry]["symbol"].unique()
    for ticker in list_of_tickers:
        url = r"https://financialmodelingprep.com/api/v3/company-key-metrics/%s" % ticker
        metrics = pd.read_json(url)
        if len(metrics) > 0:
            metrics.drop("symbol", axis=1, inplace=True)
            data = []
            for i in range(metrics.shape[0]):
                data.append(metrics.iloc[i][0])
            df_m = pd.DataFrame(data).T
            df_m.columns = [i[:4] for i in pd.DataFrame(data).T.loc["date"]]
            df_m.drop("date", axis=0, inplace=True)
            df_m["symbol"] = ticker
            df_m["industry"] = industry
            df_m = df_m.loc[:, ~df_m.columns.duplicated()]
            df_m = df_m.loc[index_keep]
            df = pd.concat([df, df_m], axis=0, sort=True)

    # Print statement for check
    industries_processed.append(industry)
    if len(industries_processed)%10 == 0:
        print("Processed so far ", len(industries_processed))

df.fillna(0, inplace=True)
df = df.reset_index().rename(columns={"index": "line_item"})
df.to_csv("data/df_metrics_full.csv", index=False)