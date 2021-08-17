import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from ...models import BalanceSheetStatement, CashFlowStatement, IncomeStatement
import datetime


class Command(BaseCommand):
    help = 'Populates the Database with the annual financial data'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        cash_flow_statements_df = pd.DataFrame(
            list(CashFlowStatement.objects.all().values()))
        income_statement_df = pd.DataFrame(
            list(IncomeStatement.objects.all().values()))
        balance_sheet_statement_df = pd.DataFrame(
            list(BalanceSheetStatement.objects.all().values()))

        print(cash_flow_statements_df)
        print(income_statement_df)
        print(balance_sheet_statement_df)
        breakpoint()
        # Pull data from DB for current year, previous year, 2 years ago.
        # Compile dataframes of all required data
        # Run analysis
        symbol = "NVDA"
        quantity = 100
        price = 352
        return symbol, quantity, price
