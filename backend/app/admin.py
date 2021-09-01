from .models import (
    BalanceSheetStatement,
    CashFlowStatement,
    CompanyProfile,
    MagicFormulaScore,
    SAndP500,
    IncomeStatement,
    PiotroskiScore,
)
from django.contrib import admin


class StockList(admin.ModelAdmin):
    list_display = ("symbol", "name", "sector")


class FinancialData(admin.ModelAdmin):
    list_display = ("symbol", "date")


class StockRating(admin.ModelAdmin):
    list_display = ("symbol", "totalScore")


class CompanyProfileData(admin.ModelAdmin):
    list_display = ("symbol", "exchangeShortName")


class MagicFormulaScoreData(admin.ModelAdmin):
    list_display = (
        "symbol",
        "earningYield",
        "returnOnCapital",
        "forwardAnnualDividendYield",
        "magicFormulaRank",
    )


# Register your models here.
admin.site.register(SAndP500, StockList)
admin.site.register(IncomeStatement, FinancialData)
admin.site.register(BalanceSheetStatement, FinancialData)
admin.site.register(CashFlowStatement, FinancialData)
admin.site.register(PiotroskiScore, StockRating)
admin.site.register(CompanyProfile, CompanyProfileData)
admin.site.register(MagicFormulaScore, MagicFormulaScoreData)
