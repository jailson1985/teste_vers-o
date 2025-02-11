import pandas as pd
import statsmodels.api as sm
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    Conta,
    ContaContabil,
    ModelForecastEmployment,
    ModelForecastKeep,
    ModelForecastContabil,
    ModelForecastCcusto,
    VariacaoDolar
)
from .serializers import (
    ContaSerializer,
    ContaContabilSerializer,
    ModelForecastEmploymentSerializer,
    ModelForecastKeepSerializer,
    ModelForecastContabilSerializer,
    ModelForecastCcustoSerializer,
    VariacaoDolarSerializer
)


class ContaListView(APIView):
    def get(self, request):
        contas = Conta.objects.all()
        serializer = ContaSerializer(contas, many=True)
        return Response(serializer.data)

class ContaContabilListView(APIView):
    def get(self, request):
        contas_contabil = ContaContabil.objects.all()
        serializer = ContaContabilSerializer(contas_contabil, many=True)
        return Response(serializer.data)

class ModelForecastEmploymentListView(APIView):
    def get(self, request):
        forecasts_employment = ModelForecastEmployment.objects.all()
        serializer = ModelForecastEmploymentSerializer(forecasts_employment, many=True)
        return Response(serializer.data)

class ModelForecastKeepListView(APIView):
    def get(self, request):
        forecasts_keep = ModelForecastKeep.objects.all()
        serializer = ModelForecastKeepSerializer(forecasts_keep, many=True)
        return Response(serializer.data)

class ModelForecastContabilListView(APIView):
    def get(self, request):
        forecasts_contabil = ModelForecastContabil.objects.all()
        serializer = ModelForecastContabilSerializer(forecasts_contabil, many=True)
        return Response(serializer.data)

class ModelForecastCcustoListView(APIView):
    def get(self, request):
        forecasts_ccusto = ModelForecastCcusto.objects.all()
        serializer = ModelForecastCcustoSerializer(forecasts_ccusto, many=True)
        return Response(serializer.data)
    
# View para obter as variações do dólar
class VariacaoDolarAPIView(APIView):
    def get(self, request):
        # Obtemos os dados do banco de dados
        variacoes = VariacaoDolar.objects.all().order_by('data')
        serializer = VariacaoDolarSerializer(variacoes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class IPCAAPIView(APIView):
    def get(self, request):
        try:
            # A URL da API do IBGE para pegar os dados históricos do IPCA
            url = 'https://api.ibge.gov.br/indicadores/2344'
            response = requests.get(url)

            # Se a resposta for bem-sucedida (status_code == 200)
            if response.status_code == 200:
                data = response.json()  # Converte a resposta para JSON
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Não foi possível obter os dados do IPCA.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class ContaContabilAnalysisAPIView(APIView):
    def get(self, request):
        # Carregar os dados da tabela ContaContabil para um DataFrame do Pandas
        conta_contabil_data = ContaContabil.objects.all().values()
        conta_contabil_df = pd.DataFrame(conta_contabil_data)

        # Verificando tipos de dados
        print(conta_contabil_df.dtypes)

        # Tratando valores NaN e forçando a conversão para numérico
        conta_contabil_df['valor_realizado'] = pd.to_numeric(conta_contabil_df['valor_realizado'], errors='coerce')
        conta_contabil_df['ano'] = pd.to_numeric(conta_contabil_df['ano'], errors='coerce')
        conta_contabil_df['mes'] = pd.to_numeric(conta_contabil_df['mes'], errors='coerce')

        # Substituindo NaN por 0
        conta_contabil_df['valor_realizado'].fillna(0, inplace=True)
        conta_contabil_df['ano'].fillna(conta_contabil_df['ano'].mean(), inplace=True)

        # Garantir que valores infinitos ou NaN não sejam retornados
        conta_contabil_df.replace([float('inf'), float('-inf')], float('nan'), inplace=True)

        # Garantir que os valores numéricos são válidos
        conta_contabil_df = conta_contabil_df[conta_contabil_df['valor_realizado'].notna()]
        conta_contabil_df = conta_contabil_df[conta_contabil_df['ano'].notna()]

        # Estatísticas descritivas básicas
        conta_contabil_desc = conta_contabil_df.describe(include=[float, int])

        # Ajuste de um modelo de regressão linear
        X = conta_contabil_df[['ano']]  # Variável independente (ano)
        X = sm.add_constant(X)  # Adiciona a constante para o modelo de regressão
        y = conta_contabil_df['valor_realizado']  # Variável dependente (valor_realizado)

        # Ajustando um modelo de regressão linear
        model = sm.OLS(y, X).fit()

        # Gerando o resumo do modelo de forma mais estruturada
        model_summary_df = self.model_summary_to_dataframe(model)

        # Retorno da resposta
        return Response({
            "conta_contabil_desc": conta_contabil_desc.to_dict(),  # Descrição estatística
            "model_summary": model_summary_df.to_dict()  # Resumo estruturado do modelo de regressão
        }, status=status.HTTP_200_OK)

    def model_summary_to_dataframe(self, model):
        """
        Converte o resumo do modelo para um DataFrame organizado com as métricas principais.
        """
        # Obtendo o resumo do modelo como um dataframe
        summary_df = pd.DataFrame({
            'Coeficiente': model.params,
            'Erro Padrão': model.bse,
            't-valor': model.tvalues,
            'P>|t|': model.pvalues,
            'Intervalo Inferior (95%)': model.conf_int()[0],
            'Intervalo Superior (95%)': model.conf_int()[1]
        })

        # Organizando e formatando a tabela
        summary_df = summary_df.reset_index()
        summary_df.columns = ['Variável', 'Coeficiente', 'Erro Padrão', 't-valor', 'P>|t|', 'Intervalo Inferior (95%)', 'Intervalo Superior (95%)']

        # Ajustando a visualização para facilitar o entendimento
        summary_df = summary_df.round({
            'Coeficiente': 4,
            'Erro Padrão': 4,
            't-valor': 4,
            'P>|t|': 4,
            'Intervalo Inferior (95%)': 4,
            'Intervalo Superior (95%)': 4
        })

        return summary_df
