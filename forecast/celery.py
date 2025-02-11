from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forecast.settings')

# Cria a instância do Celery
app = Celery('forecast')

# Usa o backend Redis para enviar e receber resultados de tarefas
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carrega os módulos de tarefas registrados no Django app
app.autodiscover_tasks()
