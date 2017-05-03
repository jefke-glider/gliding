"""
Django settings for ia_rep project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e07rwrgj2_@ya^^@0lyi*21pjn^y2ls9)&rhr@96u%47^l228-'

# SECURITY WARNING: don't run with debug turned on in production!
if os.uname()[1] == 'gimli':
    DEBUG = False
    EMAIL_HOST='localhost'
    ALLOWED_HOSTS = ['air.lvzc.be']
else:
    DEBUG = True
    EMAIL_HOST = 'wall-e'
    ALLOWED_HOSTS = ['localhost']



# Application definition

INSTALLED_APPS = [
    'report_ia',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'jquery',
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

ROOT_URLCONF = 'ia_rep.urls'

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

WSGI_APPLICATION = 'ia_rep.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE' : 'django.db.backends.postgresql',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME' : 'ato_ia',
        'USER': 'ato_admin',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = '/report_ia/'
#LOGIN_URL = 'user/login/'

#AUTH_PROFILE_MODULE = 'report_ia.UserProfile'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'nl-nl'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = False
DATE_FORMAT = "d/m/Y"
SHORT_DATE_FORMAT = "d/m/Y"
DATE_INPUT_FORMATS = (
    '%d/%m/%Y',  # '25/10/2006'
    # '%b %d %Y', '%b %d, %Y',            # 'Oct 25 2006', 'Oct 25, 2006'
    # '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
    # '%B %d %Y', '%B %d, %Y',            # 'October 25 2006', 'October 25, 2006'
    # '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
    )


USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

if os.uname()[1] == 'gimli':
    STATIC_ROOT = '/home/jpe/gliding/ato/static/'
    MEDIA_ROOT = '/home/jpe/gliding/ato/media/'            
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'                
    STATICFILES_DIRS = [
        '/home/jpe/atoenv/lib/python3.4/site-packages/django/contrib/admin/static/'
        ]
    SESSION_COOKIE_AGE = 7200
else:
    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
        '/usr/lib/python3.4/site-packages/jquery/',
        '/home/jpe/proj/ato/ato/static/'
        ]
    MEDIA_ROOT = '/home/jpe/proj/ato/ato/media/'
    MEDIA_URL = '/media/'


