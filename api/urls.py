from django.urls import path
from .views import (
    ContaContabilAnalysisAPIView,
    ContaListView,
    ContaContabilListView,
    IPCAAPIView,
    ModelForecastEmploymentListView,
    ModelForecastKeepListView,
    ModelForecastContabilListView,
    ModelForecastCcustoListView,
    VariacaoDolarAPIView,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuração do Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="API Forecast",
      default_version='v1',
      description="API para gestão de previsões financeiras e contábeis",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@forecast.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   #permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/get_variacao-dolar/', VariacaoDolarAPIView.as_view(), name='variacao_dolar_api'),
    path('api/get_contas/', ContaListView.as_view(), name='contas-list'),
    path('api/get_contas-contabil/', ContaContabilListView.as_view(), name='contas-contabil-list'),
    path('api/get_forecast-employment/', ModelForecastEmploymentListView.as_view(), name='forecast-employment-list'),
    path('api/get_forecast-keep/', ModelForecastKeepListView.as_view(), name='forecast-keep-list'),
    path('api/get_forecast-contabil/', ModelForecastContabilListView.as_view(), name='forecast-contabil-list'),
    path('api/get_forecast-ccusto/', ModelForecastCcustoListView.as_view(), name='forecast-ccusto-list'),
    path('api/get_taxa_ipca/', IPCAAPIView.as_view(), name='ipca_api'),
    path('api/conta-contabil/analysis/', ContaContabilAnalysisAPIView.as_view(), name='conta-contabil-analysis'),

]
