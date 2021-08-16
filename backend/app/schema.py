import graphene
from graphene_django import DjangoObjectType
from .models import BalanceSheetStatement, CashFlowStatement, IncomeStatement


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


class Query(graphene.ObjectType):

    income_statements = graphene.List(IncomeStatementType)
    balance_sheet_statements = graphene.List(BalanceSheetStatementType)
    cash_flow_statements = graphene.List(CashFlowStatementType)

    def resolve_income_statements(root, info):
        return IncomeStatement.objects.all()

    def resolve_balance_sheet_statements(root, info):
        return BalanceSheetStatement.objects.all()

    def resolve_cash_flow_statements(root, info):
        return CashFlowStatement.objects.all()


schema = graphene.Schema(query=Query)
