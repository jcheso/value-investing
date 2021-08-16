from .models import BalanceSheetStatement, CashFlowStatement, SAndP500, IncomeStatement
from django.contrib import admin


class StockList(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'sector')


class FinancialData(admin.ModelAdmin):
    list_display = ('symbol', 'date')


# Register your models here.
admin.site.register(SAndP500, StockList)
admin.site.register(IncomeStatement, FinancialData)
admin.site.register(BalanceSheetStatement, FinancialData)
admin.site.register(CashFlowStatement, FinancialData)
