import graphene
from graphene_django import DjangoObjectType
from .models import Category, Product, IncomeStatement


class IncomeStatementType(DjangoObjectType):

    class Meta:
        model = IncomeStatement
        fields = '__all__'


class Query(graphene.ObjectType):

    income_statements = graphene.List(IncomeStatementType)

    def resolve_income_statements(root, info):
        return IncomeStatement.objects.all()


schema = graphene.Schema(query=Query)
