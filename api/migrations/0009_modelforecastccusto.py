# Generated by Django 5.1.5 on 2025-01-22 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_modelforecastcontabil'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelForecastCcusto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cd_empresa', models.CharField(max_length=20)),
                ('descricao_conta_contabil', models.CharField(max_length=255)),
                ('desc_centro_custo', models.CharField(max_length=255)),
                ('ano', models.IntegerField()),
                ('mes', models.IntegerField()),
                ('valor_previsto_mes_1', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('valor_previsto_mes_2', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('valor_previsto_mes_3', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('valor_previsto_mes_4', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('valor_previsto_mes_5', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('valor_previsto_mes_6', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
            ],
            options={
                'db_table': 'staging_forecast_ccusto',
            },
        ),
    ]
