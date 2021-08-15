from django.db import models
from django.utils import timezone
# Create your models here.


class IncomeStatement(models.Model):
    class Meta:
        db_table = 'app_incomestatement'  # This tells Django where the SQL table is
        managed = False  # Use this if table already exists
        # and doesn't need to be managed by Django

    date = models.DateField(default=timezone.now)
    symbol = models.CharField(max_length=255)
    index = models.IntegerField(default=0)
    reportedCurrency = models.CharField(max_length=255, default="USD")
    fillingDate = models.DateTimeField(default=timezone.now)
    acceptedDate = models.DateTimeField(default=timezone.now)
    period = models.CharField(max_length=255)
    revenue = models.BigIntegerField(default=0)
    costOfRevenue = models.BigIntegerField(default=0)
    grossProfit = models.BigIntegerField(default=0)
    grossProfitRatio = models.FloatField(default=0)
    researchAndDevelopmentExpenses = models.BigIntegerField(default=0)
    generalAndAdministrativeExpenses = models.BigIntegerField(default=0)
    sellingAndMarketingExpenses = models.BigIntegerField(default=0)
    sellingGeneralAndAdministrativeExpenses = models.BigIntegerField(default=0)
    otherExpenses = models.BigIntegerField(default=0)
    operatingExpenses = models.BigIntegerField(default=0)
    costAndExpenses = models.BigIntegerField(default=0)
    interestExpense = models.BigIntegerField(default=0)
    depreciationAndAmortization = models.BigIntegerField(default=0)
    ebitda = models.BigIntegerField(default=0)
    ebitdaratio = models.FloatField(default=0)
    operatingIncome = models.BigIntegerField(default=0)
    operatingIncomeRatio = models.FloatField(default=0)
    totalOtherIncomeExpensesNet = models.BigIntegerField(default=0)
    incomeBeforeTax = models.BigIntegerField(default=0)
    incomeBeforeTaxRatio = models.FloatField(default=0)
    incomeTaxExpense = models.BigIntegerField(default=0)
    netIncome = models.BigIntegerField(default=0)
    netIncomeRatio = models.FloatField(default=0)
    eps = models.FloatField(default=0)
    epsdiluted = models.FloatField(default=0)
    weightedAverageShsOut = models.BigIntegerField(default=0)
    weightedAverageShsOutDil = models.BigIntegerField(default=0)
    link = models.CharField(max_length=255)
    finalLink = models.CharField(max_length=255)

    def __str__(self):
        return self.symbol
