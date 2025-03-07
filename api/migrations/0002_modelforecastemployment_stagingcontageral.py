# Generated by Django 5.1.5 on 2025-01-21 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelForecastEmployment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cd_empresa', models.CharField(max_length=20)),
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
                'db_table': 'model_forecast_employment',
            },
        ),
        migrations.CreateModel(
            name='StagingContaGeral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cd_empresa', models.CharField(max_length=20)),
                ('nr_nivel', models.IntegerField()),
                ('cd_conta_sup', models.CharField(max_length=20)),
                ('ds_titulo_sup', models.CharField(max_length=255)),
                ('cd_classif_contab', models.CharField(max_length=20)),
                ('cd_conta_reduz', models.CharField(max_length=20)),
                ('ds_conta', models.CharField(max_length=255)),
                ('cd_estabelecimento', models.CharField(max_length=20)),
                ('classificacao_conta', models.CharField(max_length=50)),
                ('cod_conta_contabil', models.CharField(max_length=50)),
                ('descricao_conta_contabil', models.CharField(max_length=255)),
                ('cod_centro_custo', models.CharField(max_length=50)),
                ('desc_centro_custo', models.CharField(max_length=255)),
                ('ano', models.IntegerField()),
                ('mes', models.IntegerField()),
                ('valor_realizado', models.DecimalField(decimal_places=2, max_digits=15)),
            ],
            options={
                'db_table': 'staging_conta_geral',
            },
        ),
    ]
