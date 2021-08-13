from .models import Category, Product, IncomeStatement
from django.contrib import admin

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(IncomeStatement)
