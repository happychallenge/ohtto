
from .common import *

DEBUG = True

# INSTALLED_APPS += ['debug_toolbar',]

# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]

INTERNAL_IPS = ["127.0.0.1"] # NOTE: djanog_debug_toolbar 용 설정 추가

STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static')
STATICFILES_DIRS = (
  join(BASE_DIR, 'staticfiles/'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR,  'media')

################################
# For Local AWS S3
################################

# INSTALLED_APPS += ['storages', ]  # senty 에러로깅을 위한 추가

# AWS_ACCESS_KEY_ID = 'AKIAJYUHDGYF4ME4MRLQ'
# AWS_SECRET_ACCESS_KEY = '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'
# AWS_STORAGE_BUCKET_NAME = 'ohtto'

# STATICFILES_STORAGE = 'simpleMap.storages.StaticS3Boto3Storage'
# DEFAULT_FILE_STORAGE = 'simpleMap.storages.MediaS3Boto3Storage'

