"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ix_7xi&8(a$su%9wchw+z9tp-##2jd-auu^z(@cz%g*i$n=_3g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition


#发送邮箱验证码
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "a634831867@163.com"
EMAIL_HOST_PASSWORD = "UIWBVYAHEIHFWPPF"
EMAIL_USE_TLS = True
EMAIL_FROM = "a634831867@163.com"


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'captcha',
    'ckeditor',
    'ckeditor_uploader',

]

# 图像验证码格式，可以自定义。
CAPTCHA_OUTPUT_FORMAT = u'%(text_field)s  %(image)s %(hidden_field)s'
# 添加干扰点、干扰线
CAPTCHA_NOISE_FUNCTIONS = (
    'captcha.helpers.noise_null',
    'captcha.helpers.noise_arcs',  # 干扰线
    'captcha.helpers.noise_dots',  # 干扰点
)
# 图片大小
CAPTCHA_IMAGE_SIZE = (100, 25)
# 背景颜色
CAPTCHA_BACKGROUND_COLOR = '#ffffff'
# 验证码的样式
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'  # 随机字符
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'    # 数学表达式
# 字符个数
CAPTCHA_LENGTH = 4
# 超时时间（分钟）
CAPTCHA_TIMEOUT = 1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
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
    },
]

WSGI_APPLICATION = 'web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dianshang',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': 'Qq2442402635*',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
#配置静态文件路由
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, '/static/'),)
# 上传图片的路径
IMG_UPLOAD = os.path.join(BASE_DIR, 'static/uploads')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CKEDITOR_UPLOAD_PATH = 'item_img/'

CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_ALLOW_NONIMAGE_FILES = False


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
