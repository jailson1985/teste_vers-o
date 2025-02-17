import pandas as pd
import statsmodels.api as sm
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import pandas as pd
import numpy as np
import logging
from statsmodels.tsa.statespace.sarimax import SARIMAX
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




# Dados de IPCA e variação do Dólar de 2020 a 2024 (valores anuais aproximados)
ipca_2020_2024 = [0.323, 0.375, 0.325, 0.579, 0.502]  # IPCA de 2020 a 2024 (em %)
dolar_2020_2024 = [2.356, 0.93, 0.36, 0.82, 0.74]  # Taxa de variação do dólar anual (%) (valores aproximados)

# Função de teste de estacionariedade
def testar_estacionariedade(series):
    from statsmodels.tsa.stattools import adfuller
    result = adfuller(series)
    return result[1] <= 0.05

# Função de cálculo de valores planejados (apenas um exemplo)
def calcular_valores_planejados_por_mes(df_empresa):
    mean_month = df_empresa.groupby('mes')['valor_realizado'].mean()
    return {
        f"valor_planejado_mes_{i+1}": mean_month.get(i+1, 0) for i in range(12)  # Agora para 12 meses
    }



class PrevisaoSARIMAXCCusto(APIView):
    
    @swagger_auto_schema(
        operation_description="Previsão de custos utilizando o modelo SARIMAX",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ano_inicial': openapi.Schema(type=openapi.TYPE_INTEGER, description='Ano inicial para previsão', default=2020),
                'ano_final': openapi.Schema(type=openapi.TYPE_INTEGER, description='Ano final para previsão', default=2024),
                'incluir_variaveis': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Incluir variáveis exógenas como IPCA e variação do dólar', default=True),
            }
        ),
        responses={
            200: openapi.Response('Sucesso', openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT))),
            400: 'Parâmetros inválidos',
        }
    )
    def post(self, request):
        # Obtendo parâmetros do corpo da requisição (filtros de ano e inclusão de variáveis)
        ano_inicial = int(request.data.get('ano_inicial', 2020))  # Default é 2020
        ano_final = int(request.data.get('ano_final', 2024))  # Default é 2024
        incluir_variaveis = bool(request.data.get('incluir_variaveis', True))  # Default é incluir as variáveis

        # Filtrando os dados pelo ano inicial e final
        data = ContaContabil.objects.filter(ano__gte=ano_inicial, ano__lte=ano_final).values('cd_empresa', 'descricao_conta_contabil', 'desc_centro_custo', 'ano', 'mes', 'valor_realizado')
        df = pd.DataFrame(data)
        df['valor_realizado'] = pd.to_numeric(df['valor_realizado'], errors='coerce')
        df['data'] = pd.to_datetime(df[['ano', 'mes']].astype(str).agg('-'.join, axis=1), format='%Y-%m')
        df.set_index('data', inplace=True)

        # Criar DataFrame para IPCA e Variação do Dólar, se necessário
        if incluir_variaveis:
            df_ipca = pd.DataFrame({
                'data': pd.date_range(start=f'{ano_inicial}-01-01', end=f'{ano_final}-12-01', freq='MS'),  # Início de cada mês
                'taxa_ipca': np.repeat(ipca_2020_2024, 12)  # Repetir os valores de IPCA por ano
            })
            df_dolar = pd.DataFrame({
                'data': pd.date_range(start=f'{ano_inicial}-01-01', end=f'{ano_final}-12-01', freq='MS'),  # Início de cada mês
                'taxa_dolar': np.repeat(dolar_2020_2024, 12)  # Repetir os valores de variação do dólar por ano
            })

            # Juntar IPCA e Dólar ao DataFrame original
            df = df.join(df_ipca.set_index('data')['taxa_ipca'], on='data')
            df = df.join(df_dolar.set_index('data')['taxa_dolar'], on='data')

        # Agrupar por empresa, conta contábil e centro de custo
        grupos = df.groupby(['cd_empresa', 'descricao_conta_contabil', 'desc_centro_custo'])

        # Configuração de logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        resultados = []
        
        for (empresa, descricao_conta_contabil, desc_centro_custo), df_empresa in grupos:
            try:
                # Testar estacionariedade
                if not testar_estacionariedade(df_empresa['valor_realizado']):
                    df_empresa['valor_realizado'] = df_empresa['valor_realizado'].diff().dropna()
                    if not testar_estacionariedade(df_empresa['valor_realizado']):
                        logger.warning(f"A série de {empresa} - {descricao_conta_contabil} - {desc_centro_custo} ainda não é estacionária após diferenciação.")
                        continue

                # Definir variáveis exógenas, se necessário
                if incluir_variaveis:
                    exog = df_empresa[['taxa_dolar', 'taxa_ipca']]
                else:
                    exog = None

                # Dividir em treino e teste
                train = df_empresa['valor_realizado'][:-12]  # Usando os dados até o mês anterior
                test = df_empresa['valor_realizado'][-12:]  # Últimos 12 meses para teste (não usado na previsão)

                # Ajustar o modelo SARIMAX
                model = SARIMAX(train, exog=exog[:-12] if exog is not None else None, order=(5, 1, 0), seasonal_order=(1, 1, 0, 12))
                model_fit = model.fit()

                # Previsão para 12 meses
                forecast = model_fit.forecast(steps=12, exog=exog[-12:] if exog is not None else None)

                logger.info(f"Previsão para empresa {empresa} - conta Contábil {descricao_conta_contabil} - CC {desc_centro_custo}:")
                logger.info(forecast)

                # Calcular valores planejados para os 12 meses
                valores_planejados = calcular_valores_planejados_por_mes(df_empresa)

                # Gravar previsões na tabela
                resultados.append({
                    "empresa": empresa,
                    "descricao_conta_contabil": descricao_conta_contabil,
                    "desc_centro_custo": desc_centro_custo,
                    "ano": df_empresa['ano'].max(),
                    "mes": df_empresa['mes'].max(),
                    "forecast": forecast.tolist(),
                    "valores_planejados": valores_planejados,
                })
            except Exception as e:
                logger.error(f"Erro ao processar empresa {empresa} - conta contábil {descricao_conta_contabil} - CC {desc_centro_custo}: {str(e)}")

        return Response(resultados, status=status.HTTP_200_OK)
