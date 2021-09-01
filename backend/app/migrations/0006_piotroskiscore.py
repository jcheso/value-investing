# Generated by Django 3.2.6 on 2021-08-18 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0005_auto_20210817_1707"),
    ]

    operations = [
        migrations.CreateModel(
            name="PiotroskiScore",
            fields=[
                (
                    "symbol",
                    models.CharField(
                        default="key", max_length=255, primary_key=True, serialize=False
                    ),
                ),
                ("operatingCashFlow", models.IntegerField(default=0)),
                ("changeInReturnOnAssets", models.IntegerField(default=0)),
                ("accruals", models.IntegerField(default=0)),
                ("leverage", models.IntegerField(default=0)),
                ("liquidity", models.IntegerField(default=0)),
                ("dilution", models.IntegerField(default=0)),
                ("grossMargin", models.IntegerField(default=0)),
                ("assetTurnoverRatio", models.IntegerField(default=0)),
                ("totalScore", models.IntegerField(default=0)),
                ("returnOnAssets", models.BigIntegerField(default=0)),
            ],
            options={
                "verbose_name": "Piotroski Score",
                "db_table": "app_piotroskiscore",
            },
        ),
    ]