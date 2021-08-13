import graphene
from graphene_django import DjangoObjectType
from .models import Category, Product, IncomeStatement


class IncomeStatementType(DjangoObjectType):

    class Meta:
        model = IncomeStatement
        fields = '__all__'


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "description", "products")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "category", 'price', 'quantity')


class Query(graphene.ObjectType):
    products = graphene.List(
        ProductType,  category=graphene.String(required=False))
    categories = graphene.List(CategoryType)
    income_statements = graphene.List(IncomeStatementType)

    def resolve_products(root, info, category=None):
        if category:
            return Product.objects.filter(category__name=category)
       # We can easily optimize query count in the resolve method
        return Product.objects.select_related("category").all()

    def resolve_categories(root, info):
        return Category.objects.all()

    def resolve_income_statements(root, info):
        return IncomeStatement.objects.all()


schema = graphene.Schema(query=Query)
