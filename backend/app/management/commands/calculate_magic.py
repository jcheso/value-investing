from sqlalchemy import create_engine
from django.conf import settings
import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from ...models import (
    BalanceSheetStatement,
    CashFlowStatement,
    IncomeStatement,
    CompanyProfile,
    SAndP500,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = settings.DATABASES["default"]["USER"]
        password = settings.DATABASES["default"]["PASSWORD"]
        database_name = settings.DATABASES["default"]["NAME"]

        database_url = "postgresql://{user}:{password}@ec2-44-195-201-3.compute-1.amazonaws.com:5432/{database_name}".format(
            user=user,
            password=password,
            database_name=database_name,
        )

        engine = create_engine(database_url, echo=False)

        # cash_flow_statement_df = pd.read_sql("app_cashflowstatement", engine)
        # income_statement_df = pd.read_sql("app_incomestatement", engine)
        # balance_sheet_statement_df = pd.read_sql("app_balancesheetstatement", engine)
        # share_index_df = pd.read_sql("app_sandp500", engine)
        # company_profile_df = pd.read_sql("app_companyprofile", engine)

        cash_flow_statement_df = pd.DataFrame(
            list(CashFlowStatement.objects.all().values())
        )
        income_statement_df = pd.DataFrame(list(IncomeStatement.objects.all().values()))
        balance_sheet_statement_df = pd.DataFrame(
            list(BalanceSheetStatement.objects.all().values())
        )
        share_index_df = pd.DataFrame(list(SAndP500.objects.all().values()))
        company_profile_df = pd.DataFrame(list(CompanyProfile.objects.all().values()))

        # Drop unnecessary columns
        balance_sheet_statement_df.drop(
            ["fillingDate", "acceptedDate", "period", "link", "finalLink"],
            inplace=True,
            axis=1,
        )
        income_statement_df.drop(
            [
                "fillingDate",
                "acceptedDate",
                "period",
                "link",
                "finalLink",
                "date",
                "reportedCurrency",
            ],
            inplace=True,
            axis=1,
        )
        cash_flow_statement_df.drop(
            [
                "netIncome",
                "fillingDate",
                "acceptedDate",
                "period",
                "link",
                "finalLink",
                "date",
                "depreciationAndAmortization",
            ],
            inplace=True,
            axis=1,
        )

        # Separate each DF by year and merge financial data
        temp_balance_sheet_statement_df = balance_sheet_statement_df.loc[
            balance_sheet_statement_df["index"] == 0
        ]
        temp_balance_sheet_statement_df.set_index("symbol", inplace=True)
        temp_balance_sheet_statement_df.drop(
            ["index"],
            inplace=True,
            axis=1,
        )

        temp_income_statement_df = income_statement_df.loc[
            income_statement_df["index"] == 0
        ]
        temp_income_statement_df.set_index("symbol", inplace=True)
        temp_income_statement_df.drop(
            ["index"],
            inplace=True,
            axis=1,
        )

        temp_cash_flow_statement_df = cash_flow_statement_df.loc[
            cash_flow_statement_df["index"] == 0
        ]
        temp_cash_flow_statement_df.set_index("symbol", inplace=True)
        temp_cash_flow_statement_df.drop(
            ["index"],
            inplace=True,
            axis=1,
        )

        company_profile_df.set_index("symbol", inplace=True)

        df_cy = pd.concat(
            [
                temp_balance_sheet_statement_df,
                temp_income_statement_df,
                temp_cash_flow_statement_df,
                company_profile_df,
            ],
            axis=1,
        )

        symbols = share_index_df["symbol"]

        # calculating relevant financial metrics for each stock
        final_stats_df = pd.DataFrame()
        final_stats_df["EBIT"] = df_cy["ebitda"] - df_cy["depreciationAndAmortization"]
        final_stats_df["TEV"] = (
            df_cy["mktCap"]
            + df_cy["longTermDebt"].fillna(0)
            - (df_cy["totalCurrentAssets"] - df_cy["totalCurrentLiabilities"].fillna(0))
        )
        final_stats_df["earningYield"] = final_stats_df["EBIT"] / final_stats_df["TEV"]
        final_stats_df["FCFYield"] = (
            df_cy["netCashProvidedByOperatingActivities"] - df_cy["capitalExpenditure"]
        ) / df_cy["mktCap"]
        final_stats_df["returnOnCapital"] = (
            df_cy["ebitda"] - df_cy["depreciationAndAmortization"]
        ) / (
            df_cy["propertyPlantEquipmentNet"]
            + df_cy["totalCurrentAssets"]
            - df_cy["totalCurrentLiabilities"]
        )
        final_stats_df["bookToMkt"] = df_cy["totalStockholdersEquity"] / df_cy["mktCap"]
        final_stats_df["forwardAnnualDividendYield"] = df_cy["lastDiv"] / df_cy["price"]

        ################################Output Dataframes##############################

        # finding value stocks based on Magic Formula
        final_stats_val_df = final_stats_df.loc[:, :]
        final_stats_val_df["CombRank"] = final_stats_val_df["earningYield"].rank(
            ascending=False, na_option="bottom"
        ) + final_stats_val_df["returnOnCapital"].rank(
            ascending=False, na_option="bottom"
        )
        final_stats_val_df["magicFormulaRank"] = final_stats_val_df["CombRank"].rank(
            method="first"
        )
        value_stocks = final_stats_val_df.sort_values("magicFormulaRank").iloc[
            :, [2, 4, 8]
        ]
        print("------------------------------------------------")
        print("Value stocks based on Greenblatt's Magic Formula")
        print(value_stocks[:10])

        final_stats_df.fillna(0, inplace=True)

        # finding highest dividend yield stocks
        high_dividend_stocks = final_stats_df.sort_values(
            "forwardAnnualDividendYield", ascending=False
        ).iloc[:, 6]
        print("------------------------------------------------")
        print("Highest dividend paying stocks")
        print(high_dividend_stocks[:10])

        # # Magic Formula & Dividend yield combined
        final_stats_df["CombRank"] = (
            final_stats_df["earningYield"].rank(ascending=False, method="first")
            + final_stats_df["returnOnCapital"].rank(ascending=False, method="first")
            + final_stats_df["forwardAnnualDividendYield"].rank(
                ascending=False, numeric_only=True, method="first"
            )
        )
        final_stats_df["CombinedRank"] = final_stats_df["CombRank"].rank(method="first")
        value_high_div_stocks = final_stats_df.sort_values("CombinedRank").iloc[
            :, [2, 4, 6, 8]
        ]
        print("------------------------------------------------")
        print("Magic Formula and Dividend Yield combined")
        print(value_high_div_stocks[:10])

        value_high_div_stocks.to_sql(
            "app_magicformulascore", con=engine, if_exists="replace"
        )
