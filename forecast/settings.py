"""
Django settings for forecast project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from celery.schedules import crontab
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$d=-y#zmp@gp_vx4&ahn!594a7ijal=oa79neqj_gbbz=d+^_@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', 
    'corsheaders',
    'django_celery_results',
    'django_celery_beat',
    'drf_yasg',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'forecast.urls'

CORS_ALLOW_ALL_ORIGINS = True  # Para permitir qualquer origem


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'forecast.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# Definindo o diretório onde os arquivos estáticos serão armazenados
STATIC_URL = '/static/'  # URL para acesso aos arquivos estáticos

# Diretório onde os arquivos estáticos serão coletados em produção
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Adicionando o diretório estático local do projeto
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configurações Celery
CELERY_BROKER_URL = 'redis://redis:6379/0'  # URL do Redis (assumindo que o Redis está rodando localmente)
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Armazenamento dos resultados das tarefas no banco de dados
CELERY_RESULT_BACKEND = 'django-db'

# Configuração do Celery Beat
CELERY_BEAT_SCHEDULE = {
    # Task para importar o arquivo XLSX de plano de contas
    'importar_xlsx_plano_conta': {
        'task': 'api.tasks.importar_xlsx_plano_conta',  # Caminho para a task
        'schedule': crontab(minute=59, hour=13),  # Intervalo de 1 minuto (60 segundos)
          # Caminho para o arquivo dentro do contêiner
        'args': (r'/app/file/Plano_de_contas.xlsx',),
    },
   'importar_xlsx_conta_contabil': {
        'task': 'api.tasks.importar_xlsx_conta_contabil',  # Caminho para a task
        'schedule': crontab(minute=54, hour=13),  # Intervalo de 1 hora (3600 segundos)
        'args': (r'/app/file/Despesas.xlsx',),
          # Argumentos para a task
    },
    'previsao_arima': {
        'task': 'api.tasks.previsao_arima_task',
        'schedule': crontab(minute=17, hour=2),  # Executar a cada 30 dias (2592000 segundos)
    },
    'previsao_arima_keep': {
        'task': 'api.tasks.previsao_arima_keep_task',
        'schedule': crontab(minute=25, hour=2),  # Executar a cada 30 dias (2592000 segundos)
    },
     'previsao_arima_contabil': {
        'task': 'api.tasks.previsao_arima_contabil_task',
        'schedule': crontab(minute=16, hour=13),  # Executar a cada 30 dias (2592000 segundos)
    },
    'previsao_arima_ccusto': {
        'task': 'api.tasks.previsao_arima_ccusto_task',
        'schedule': crontab(minute=10, hour=13),  # Executar a cada 30 dias (2592000 segundos)
    },
        'popular_variacao_dolar': {
        'task': 'api.tasks.popular_variacao_dolar',
        'schedule': crontab(minute=30, hour=23),  # Executar a cada 30 dias (2592000 segundos)
    },
}
