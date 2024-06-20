import os

from config.env import env




# Celery Configuration Options
CELERY_TIMEZONE = "Asia/Dhaka"
# timezone = "Asia/Dhaka"

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# broker_connection_retry_on_startup = True








##* Set Broker Url
# To check redis url, go to the command line and run >> redis-cli
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
# CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
# broker_url = env('CELERY_BROKER_URL')




##* Set Result Backend
# CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"
# CELERY_RESULT_BACKEND = "redis://localhost:6379"
# CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
# result_backend = env('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

CELERY_RESULT_BACKEND = 'django-db'          ##! For Database
# result_backend  = 'django-db'              ##! For Database
# CELERY_CACHE_BACKEND   = 'django-cache'    ##! For Cache 
# result_backend = 'django-cache'




CELERY_RESULT_EXTENDED = True



# Additional Celery settings
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"







