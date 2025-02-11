from django.db import models

class Conta(models.Model):
    cd_empresa = models.CharField(max_length=20)  # Código da empresa (alfanumérico)
    nr_nivel = models.IntegerField()  # Nível hierárquico (inteiro)
    cd_conta_sup = models.CharField(max_length=20)  # Código da conta superior (alfanumérico)
    ds_titulo_sup = models.CharField(max_length=255)  # Descrição do título superior (texto)
    cd_classif_contab = models.CharField(max_length=20)  # Código da classificação contábil (alfanumérico)
    cd_conta_reduz = models.CharField(max_length=20)  # Código da conta reduzida (alfanumérico)
    ds_conta = models.CharField(max_length=255)  # Descrição da conta (texto)

    class Meta:
        db_table = 'raw_plano_conta'  # Nome da tabela no banco de dados

    def __str__(self):
        return f"{self.ds_conta} - {self.cd_empresa}"


class ContaContabil(models.Model):
    cd_empresa = models.CharField(max_length=20)  # Código da empresa (alfanumérico)
    cd_estabelecimento = models.CharField(max_length=20)  # Código do estabelecimento (alfanumérico)
    classificacao_conta = models.CharField(max_length=50)  # Classificação da conta (texto)
    cod_conta_contabil = models.CharField(max_length=50)  # Código da conta contábil (alfanumérico)
    descricao_conta_contabil = models.CharField(max_length=255)  # Descrição da conta contábil (texto)
    cod_centro_custo = models.CharField(max_length=50)  # Código do centro de custo (alfanumérico)
    desc_centro_custo = models.CharField(max_length=255)  # Descrição do centro de custo (texto)
    ano = models.IntegerField()  # Ano (número inteiro)
    mes = models.IntegerField()  # Mês (número inteiro)
    valor_realizado = models.DecimalField(max_digits=15, decimal_places=2)  # Valor realizado (decimal)

    class Meta:
        db_table = 'raw_conta_contabil'  # Nome da tabela no banco de dados

    def __str__(self):
        return f"{self.descricao_conta_contabil} - {self.cd_empresa} ({self.ano}/{self.mes})"



class ModelForecastEmployment(models.Model):
    cd_empresa = models.CharField(max_length=20)  # Código da empresa (alfanumérico)
    ano = models.IntegerField()  # Ano da previsão
    mes = models.IntegerField()  # Mês da previsão
    
    # Colunas para armazenar os valores previstos para os próximos 6 meses
    valor_previsto_mes_1 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_2 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_3 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_4 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_5 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_6 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'staging_forecast_employment'  # Nome da tabela no banco de dados

    def __str__(self):
        return f"{self.cd_empresa} - {self.ano}/{self.mes}"

class ModelForecastKeep(models.Model):
    cd_empresa = models.CharField(max_length=20)  # Código da empresa (alfanumérico)
    cd_estabelecimento = models.CharField(max_length=20)  # Código do estabelecimento (alfanumérico)
    ano = models.IntegerField()  # Ano da previsão
    mes = models.IntegerField()  # Mês da previsão
    
    # Colunas para armazenar os valores previstos para os próximos 6 meses
    valor_previsto_mes_1 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_2 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_3 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_4 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_5 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_6 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'staging_forecast_keep'  # Nome da tabela no banco de dados

    def __str__(self):
        return f"{self.cd_empresa} - {self.ano}/{self.mes}"


class ModelForecastContabil(models.Model):
    cd_empresa = models.CharField(max_length=20)  # Código da empresa (alfanumérico)
    descricao_conta_contabil = models.CharField(max_length=255) 
    ano = models.IntegerField()  # Ano da previsão
    mes = models.IntegerField()  # Mês da previsão
    
    # Colunas para armazenar os valores previstos para os próximos 6 meses
    valor_previsto_mes_1 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_2 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_3 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_4 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_5 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_6 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'staging_forecast_contabil'  # Nome da tabela no banco de dados

    def __str__(self):
        return f"{self.cd_empresa} - {self.ano}/{self.mes}"
    
class ModelForecastCcusto(models.Model):
    cd_empresa = models.CharField(max_length=20)  # Código da empresa (alfanumérico)
    descricao_conta_contabil = models.CharField(max_length=255)
    desc_centro_custo = models.CharField(max_length=255)
    ano = models.IntegerField()  # Ano da previsão
    mes = models.IntegerField()  # Mês da previsão

    # Colunas para armazenar os valores previstos para os próximos 6 meses
    valor_previsto_mes_1 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_2 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_3 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_4 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_5 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_previsto_mes_6 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    # Colunas para armazenar os valores planejados para os próximos 6 meses
    valor_planejado_mes_1 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_planejado_mes_2 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_planejado_mes_3 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_planejado_mes_4 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_planejado_mes_5 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    valor_planejado_mes_6 = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'staging_forecast_ccusto'  # Nome da tabela no banco de dados

    def __str__(self):
        return f"{self.cd_empresa} - {self.ano}/{self.mes}"


class VariacaoDolar(models.Model):
    data = models.DateField()  # Data da cotação
    valor_dolar = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Valor do Dólar em BRL
    variacao_percentual = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Variação em %

    def __str__(self):
        return f"Dólar em {self.data}: {self.valor_dolar} BRL"

    class Meta:
        db_table = 'variacao_dolar'  # Nome da tabela no banco de dados




