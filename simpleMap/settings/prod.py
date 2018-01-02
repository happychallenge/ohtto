from .common import *

DEBUG = False

import dj_database_url

################################
# For HeroKu Deploy AWS S3 
################################
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

INSTALLED_APPS += ['storages', ]  # senty 에러로깅을 위한 추가

AWS_ACCESS_KEY_ID = 'AKIAJYUHDGYF4ME4MRLQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'ohtto'

STATICFILES_STORAGE = 'simpleMap.storages.StaticS3Boto3Storage'
DEFAULT_FILE_STORAGE = 'simpleMap.storages.MediaS3Boto3Storage'

################################
# For HeroKu Deploy Local 
################################
# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)

# STATIC_URL = '/static/'
# STATICFILES_DIRS = [ join(BASE_DIR, 'staticfiles'),]
# STATIC_ROOT = join(BASE_DIR, 'static')

# MEDIA_URL = '/media/'
# MEDIA_ROOT = join(BASE_DIR, 'media')



################################
# For HeroKu AWS S3
################################



# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)

# INSTALLED_APPS += ['storages', ]  # senty 에러로깅을 위한 추가

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# AWS_S3_SECURE_URLS =False
# AWS_QUERYSTRING_AUTH = False

# AWS_REGION = 'ap-northeast-2'
# AWS_STORAGE_BUCKET_NAME = 'ohtto'
# AWS_QUERYSTRING_AUTH = False
# AWS_S3_HOST = 's3.%s.amazonaws.com' % AWS_REGION
# AWS_ACCESS_KEY_ID = 'AKIAIWDHZGC5RTSGR4PQ'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# # Static Setting
# STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# #Media Setting
# MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
# # sentry 에러로깅 설정
# import raven

# GIT_ROOT = os.path.join(BASE_DIR, '..')
# if os.path.exists(os.path.join(GIT_ROOT, '.git')):
#     release = raven.fetch_git_sha(GIT_ROOT)  # 현재 최근 커밋해시 획득
# else:
#     release = 'dev'

# RAVEN_CONFIG = {
#     'release': release,
#     'dsn': 'https://b0a8cd152e3c48d3af2dfeae58565ea3:70a0250beaf74aafb7f394fe78ca9d6d@sentry.io/187769',
#     # If you are using git, you can also automatically configure the
#     # release based on the git info.
# }
