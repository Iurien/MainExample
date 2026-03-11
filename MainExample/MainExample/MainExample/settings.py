"""
Настройки Django для проекта MainExample\settings.py.

Сгенерировано командой 'django-admin startproject' с использованием Django 6.0.2.

Дополнительную информацию об этом файле см. по ссылке:
https://docs.djangoproject.com/en/6.0/topics/settings/

Полный список настроек и их значений см. по ссылке:
https://docs.djangoproject.com/en/6.0/ref/settings/
"""
import os
from pathlib import Path
from decouple import config

# Пути внутри проекта следует создавать следующим образом: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Настройки для быстрого запуска разработки — не подходят для использования в производственной среде
# См. https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# ПРЕДУПРЕЖДЕНИЕ О БЕЗОПАСНОСТИ: храните секретный ключ, используемый в рабочей среде, в секрете!
SECRET_KEY = 'django-insecure-kiq3q788jv=$@*ywo=&jfq=x5^_j2z7@4whf6#52ar3phk_!wh'

# ПРЕДУПРЕЖДЕНИЕ О БЕЗОПАСНОСТИ: не запускайте программу с включенной отладкой в ​​рабочей среде!
DEBUG = True

ALLOWED_HOSTS = []


# Определение приложения

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MainExample.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MainExample.wsgi.application'


# База данных
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Проверка пароля
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Интернационализация
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'Ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Статические файлы (CSS, JavaScript, изображения)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Настройки SMTP для Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jdiuran@gmail.com' # Адрес электронной почты, созданный специально для проекта.
EMAIL_HOST_PASSWORD = "qzdz fzmi gxzf bsth"  # Ваш 16-значный аароль приложения, сгенерированный в настройках Google (обычный пароль от аккаунта использовать нельзя)
DEFAULT_FROM_EMAIL = 'jdiuran@gmail.com'
# бэкенд по умолчанию
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = config("EMAIL_HOST", cast=str, default=None)
# EMAIL_PORT = config("EMAIL_PORT", cast=str, default='587') # Рекомендуется
# EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str, default=None)
# EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str, default=None)
# EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)  # Используйте EMAIL_PORT 587 для TLS.
# EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False) # Используйте MAIL_PORT 465 для SSL.

ADMIN_USER_NAME=config("Miki", default="Admin user")
ADMIN_USER_EMAIL=config("jdiuran@gmail.com", default=None)

MANAGERS=[]
ADMINS=[]
if all([ADMIN_USER_NAME, ADMIN_USER_EMAIL]):
    ADMINS +=[
        (f'{ADMIN_USER_NAME}', f'{ADMIN_USER_EMAIL}')
    ]
    MANAGERS=ADMINS

