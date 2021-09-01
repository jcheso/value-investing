# Generated by Django 3.2.6 on 2021-09-01 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_companyprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='MagicFormulaScore',
            fields=[
                ('symbol', models.CharField(default='key', max_length=255, primary_key=True, serialize=False)),
                ('earningYield', models.FloatField(default=0)),
                ('returnOnCapital', models.FloatField(default=0)),
                ('forwardAnnualDividendYield', models.FloatField(default=0)),
                ('magicFormulaRank', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Magic Formula Score',
                'db_table': 'app_magicformulascore',
            },
        ),
    ]
