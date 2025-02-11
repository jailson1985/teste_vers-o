from rest_framework import serializers
from .models import (
    Conta,
    ContaContabil,
    ModelForecastEmployment,
    ModelForecastKeep,
    ModelForecastContabil,
    ModelForecastCcusto,
    VariacaoDolar
)

class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = '__all__'

class ContaContabilSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaContabil
        fields = '__all__'

class ModelForecastEmploymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelForecastEmployment
        fields = '__all__'

class ModelForecastKeepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelForecastKeep
        fields = '__all__'

class ModelForecastContabilSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelForecastContabil
        fields = '__all__'

class ModelForecastCcustoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelForecastCcusto
        fields = '__all__'


class VariacaoDolarSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariacaoDolar
        fields = ['data', 'valor_dolar', 'variacao_percentual']