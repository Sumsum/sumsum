import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = os.environ.get('DJANGO_ENV', 'development') == 'development'


ALLOWED_HOSTS = ['*']
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
AUTH_USER_MODEL = 'users.User'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'yashop::'
    }
}
DATABASES = {'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'yashop',
}}
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'redactor',
    'debug_toolbar',
    'django_select2',
    'timezone_field',
    #'advanced_filters',

    'customers',
    'users',
    'metafields',
    'discounts',
    'orders',
    'locations',
    'products',
    'fulfillments',
    'shops',
    'pages',
    'blogs',
]
INTERNAL_IPS = ('127.0.0.1',)
LANGUAGE_CODE = 'en-us'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
MIDDLEWARE = [
    'yashop.middleware.RequestLocalMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'superuser.middleware.SuperUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
REDACTOR_OPTIONS = {'lang': 'en'}
REDACTOR_UPLOAD = 'images/'
ROOT_URLCONF = 'yashop.urls'
SECRET_KEY = os.environ.get('SECRET_KEY', 'sumSUMsum')
SELECT2_CACHE_BACKEND = 'default'
STATIC_ROOT = os.path.join(BASE_DIR, 'site_static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
WSGI_APPLICATION = 'yashop.wsgi.application'
