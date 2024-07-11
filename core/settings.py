from pathlib import Path
import os
from decouple import config
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("secret_key")
DEBUG = True
ALLOWED_HOSTS = ["*"]
SITE_ID = 1
INSTALLED_APPS = [
    # * Apps

    'articles.apps.ArticlesConfig',
    'users.apps.UsersConfig',
    'wiki.apps.WikiConfig',
    'questions.apps.QuestionsConfig',
    'api.apps.ApiConfig',
    'profiles.apps.ProfilesConfig',

    # * Libraries and Frameworks

    'tinymce',
    'rest_framework',
    'django_recaptcha',
    'mathfilters',

    # * Django Stuff

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
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
ROOT_URLCONF = 'core.urls'
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
WSGI_APPLICATION = 'core.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
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


# * Static and Media Configuration

STATIC_URL = 'static/'
STATIC_ROOT = config("static_root")
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_ROOT = config("media_root")
MEDIA_URL = '/media/'
FILE_UPLOAD_MAX_MEMORY_SIZE = 5000000

# * Email Configuration

EMAIL_BACKEND = "django_smtp_ssl.SSLEmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = config('emuser')
EMAIL_HOST_PASSWORD = config("empass")
EMAIL_PORT = 465
DEFAULT_FROM_EMAIL = config('emfrommail')
EMAIL_USE_TLS = True


# ! Security Configuration

CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_HSTS_SECONDS = 2_592_000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = 'home'
RECAPTCHA_PUBLIC_KEY = config("recaptchapub")
RECAPTCHA_PRIVATE_KEY = config("recaptchapri")
RECAPTCHA_REQUIRED_SCORE = 0.85
# CSRF_TRUSTED_ORIGINS = ['https://site.tld']

# * Libraries Configuration

TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = False

TINYMCE_JS_URL = 'https://cdn.tiny.cloud/1/' + \
    str(config("tinymce")) + '/tinymce/5/tinymce.min.js'

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "en_US",
}

# * Misc

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
