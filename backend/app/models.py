from django.db import models
from django.utils import timezone
# Create your models here.


class SAndP500(models.Model):
    class Meta:
        db_table = 'app_sandp500'
        verbose_name = 'S&P 500 Stock'

    symbol = models.CharField(max_length=255, default="key", primary_key=True)
    name = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class IncomeStatement(models.Model):
    class Meta:
        db_table = 'app_incomestatement'  # This tells Django where the SQL table is
        verbose_name = 'Income Statement'
        # managed = False  # Use this if table already exists
    # and doesn't need to be managed by Django
    index = models.IntegerField(default=0)
    date = models.DateField(max_length=255, default=timezone.now)
    symbol = models.CharField(max_length=255)
    reportedCurrency = models.CharField(max_length=255, default="USD")
    fillingDate = models.DateField(max_length=255, default=timezone.now)
    acceptedDate = models.DateField(max_length=255, default=timezone.now)
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
    link = models.URLField(max_length=200, primary_key=True, default="None")
    finalLink = models.URLField(max_length=200)

    def __str__(self):
        return self.symbol


class BalanceSheetStatement (models.Model):
    class Meta:
        # This tells Django where the SQL table is
        db_table = 'app_balancesheetstatement'
        verbose_name = 'Balance Sheet Statement'
    index = models.IntegerField(default=0)
    date = models.DateField(max_length=255, default=timezone.now)
    symbol = models.CharField(max_length=255)
    fillingDate = models.DateField(max_length=255, default=timezone.now)
    acceptedDate = models.DateField(max_length=255, default=timezone.now)
    period = models.CharField(max_length=255)
    cashAndCashEquivalents = models.BigIntegerField(default=0)
    shortTermInvestments = models.BigIntegerField(default=0)
    cashAndShortTermInvestments = models.BigIntegerField(default=0)
    netReceivables = models.BigIntegerField(default=0)
    inventory = models.BigIntegerField(default=0)
    otherCurrentAssets = models.BigIntegerField(default=0)
    totalCurrentAssets = models.BigIntegerField(default=0)
    propertyPlantEquipmentNet = models.BigIntegerField(default=0)
    goodwill = models.BigIntegerField(default=0)
    intangibleAssets = models.BigIntegerField(default=0)
    goodwillAndIntangibleAssets = models.BigIntegerField(default=0)
    longTermInvestments = models.BigIntegerField(default=0)
    taxAssets = models.BigIntegerField(default=0)
    otherNonCurrentAssets = models.BigIntegerField(default=0)
    totalNonCurrentAssets = models.BigIntegerField(default=0)
    otherAssets = models.BigIntegerField(default=0)
    totalAssets = models.BigIntegerField(default=0)
    accountPayables = models.BigIntegerField(default=0)
    shortTermDebt = models.BigIntegerField(default=0)
    taxPayables = models.BigIntegerField(default=0)
    deferredRevenue = models.BigIntegerField(default=0)
    otherCurrentLiabilities = models.BigIntegerField(default=0)
    totalCurrentLiabilities = models.BigIntegerField(default=0)
    longTermDebt = models.BigIntegerField(default=0)
    deferredRevenueNonCurrent = models.BigIntegerField(default=0)
    deferredTaxLiabilitiesNonCurrent = models.BigIntegerField(default=0)
    otherNonCurrentLiabilities = models.BigIntegerField(default=0)
    totalNonCurrentLiabilities = models.BigIntegerField(default=0)
    otherLiabilities = models.BigIntegerField(default=0)
    totalLiabilities = models.BigIntegerField(default=0)
    commonStock = models.BigIntegerField(default=0)
    retainedEarnings = models.BigIntegerField(default=0)
    accumulatedOtherComprehensiveIncomeLoss = models.BigIntegerField(default=0)
    othertotalStockholdersEquity = models.BigIntegerField(default=0)
    totalStockholdersEquity = models.BigIntegerField(default=0)
    totalLiabilitiesAndStockholdersEquity = models.BigIntegerField(default=0)
    totalInvestments = models.BigIntegerField(default=0)
    totalDebt = models.BigIntegerField(default=0),
    netDebt = models.BigIntegerField(default=0)
    link = models.URLField(max_length=200, primary_key=True, default="None")
    finalLink = models.URLField(max_length=200)


class CashFlowStatement(models.Model):
    class Meta:
        # This tells Django where the SQL table is
        db_table = 'app_cashflowstatement'
        verbose_name = 'Cash Flow Statement'
    index = models.IntegerField(default=0)
    date = models.DateField(max_length=255, default=timezone.now)
    symbol = models.CharField(max_length=255)
    fillingDate = models.DateField(max_length=255, default=timezone.now)
    acceptedDate = models.DateField(max_length=255, default=timezone.now)
    period = models.CharField(max_length=255)
    netIncome = models.BigIntegerField(default=0)
    depreciationAndAmortization = models.BigIntegerField(default=0)
    deferredIncomeTax = models.BigIntegerField(default=0)
    stockBasedCompensation = models.BigIntegerField(default=0)
    changeInWorkingCapital = models.BigIntegerField(default=0)
    accountsReceivables = models.BigIntegerField(default=0)
    inventory = models.BigIntegerField(default=0)
    accountsPayables = models.BigIntegerField(default=0)
    otherWorkingCapital = models.BigIntegerField(default=0)
    otherNonCashItems = models.BigIntegerField(default=0)
    netCashProvidedByOperatingActivities = models.BigIntegerField(default=0)
    investmentsInPropertyPlantAndEquipment = models.BigIntegerField(default=0)
    acquisitionsNet = models.BigIntegerField(default=0)
    purchasesOfInvestments = models.BigIntegerField(default=0)
    salesMaturitiesOfInvestments = models.BigIntegerField(default=0)
    otherInvestingActivites = models.BigIntegerField(default=0)
    netCashUsedForInvestingActivites = models.BigIntegerField(default=0)
    debtRepayment = models.BigIntegerField(default=0)
    commonStockIssued = models.BigIntegerField(default=0)
    commonStockRepurchased = models.BigIntegerField(default=0)
    dividendsPaid = models.BigIntegerField(default=0)
    otherFinancingActivites = models.BigIntegerField(default=0)
    netCashUsedProvidedByFinancingActivities = models.BigIntegerField(
        default=0)
    effectOfForexChangesOnCash = models.BigIntegerField(default=0)
    netChangeInCash = models.BigIntegerField(default=0)
    cashAtEndOfPeriod = models.BigIntegerField(default=0)
    cashAtBeginningOfPeriod = models.BigIntegerField(default=0)
    operatingCashFlow = models.BigIntegerField(default=0)
    capitalExpenditure = models.BigIntegerField(default=0)
    freeCashFlow = models.BigIntegerField(default=0)
    link = models.URLField(max_length=200, primary_key=True, default="None")
    finalLink = models.URLField(max_length=200)
