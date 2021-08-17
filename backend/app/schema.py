import graphene
from graphene_django import DjangoObjectType
from .models import BalanceSheetStatement, CashFlowStatement, IncomeStatement
from .scripts import generate_portfolio


class IncomeStatementType(DjangoObjectType):

    class Meta:
        model = IncomeStatement
        fields = '__all__'


class BalanceSheetStatementType(DjangoObjectType):

    class Meta:
        model = BalanceSheetStatement
        fields = '__all__'


class CashFlowStatementType(DjangoObjectType):

    class Meta:
        model = CashFlowStatement
        fields = '__all__'


class PortfolioType(graphene.ObjectType):
    strategy = graphene.String()
    value = graphene.String()
    share_index = graphene.String()
    symbol = graphene.String()
    quantity = graphene.Int()
    price = graphene.Float()


class Query(graphene.ObjectType):
    income_statements = graphene.List(IncomeStatementType)
    balance_sheet_statements = graphene.List(BalanceSheetStatementType)
    cash_flow_statements = graphene.List(CashFlowStatementType)
    generate_portfolio = graphene.Field(PortfolioType, strategy=graphene.String(
        required=True), value=graphene.String(required=True), share_index=graphene.String(required=True))

    def resolve_income_statements(root, info):
        return IncomeStatement.objects.all()

    def resolve_balance_sheet_statements(root, info):
        return BalanceSheetStatement.objects.all()

    def resolve_cash_flow_statements(root, info):
        return CashFlowStatement.objects.all()

    def resolve_generate_portfolio(root, info, strategy, value, share_index):

        strategy = strategy
        value = value
        share_index = share_index
        symbol = "TSLA"
        quantity = 19
        price = 230
        # symbol, quantity, price = generate_portfolio.get_portfolio(
        #     strategy, value, share_index)

        return PortfolioType(strategy, value, share_index, symbol, quantity, price)


schema = graphene.Schema(query=Query)
