import pandas as pd

""" get company profiles """
""" this was previously scraped by myself """

# Drop na for clean dataset
comp_prof = pd.read_csv(r"data/company_profiles.csv")
comp_prof.dropna(inplace=True)

index_keep = ['Cash and cash equivalents',
       'Long-term debt', 'Net Debt', 'Short-term debt',
       'Total assets', 'Total current assets', 'Total current liabilities',
       'Total debt', 'Total liabilities', 'Total non-current assets',
       'Total non-current liabilities', 'Total shareholders equity']

list_of_industry = comp_prof["industry"].unique()

df = pd.DataFrame()
industries_processed = []
for industry in list_of_industry:
    list_of_tickers = comp_prof[comp_prof.industry == industry]["symbol"].unique()
    for ticker in list_of_tickers:
        url = r"https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/%s" % ticker
        balance_sheet = pd.read_json(url)
        if len(balance_sheet) > 0:
            balance_sheet.drop("symbol", axis=1, inplace=True)
            data = []
            for i in range(balance_sheet.shape[0]):
                data.append(balance_sheet.iloc[i][0])
            df_bs = pd.DataFrame(data).T
            df_bs.columns = [i[:4] for i in pd.DataFrame(data).T.loc["date"]]
            df_bs.drop("date", axis=0, inplace=True)
            df_bs["symbol"] = ticker
            df_bs["industry"] = industry
            df_bs = df_bs.loc[:, ~df_bs.columns.duplicated()]
            df_bs = df_bs.loc[index_keep]
            df = pd.concat([df, df_bs], axis=0, sort=True)

    # Print statement for check
    industries_processed.append(industry)
    if len(industries_processed)%10 == 0:
        print("Processed so far ", len(industries_processed))

df.fillna(0, inplace=True)
df = df.reset_index().rename(columns={"index": "line_item"})
df.to_csv("data/df_bs_full.csv", index=False)