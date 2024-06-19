import os

from config.env import env




# Celery Configuration Options
CELERY_TIMEZONE = "Asia/Dhaka"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60




##* To check redis url, go to the command line and run >> redis-cli
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_BROKER_URL = env('CELERY_BROKER_URL')





# # Let's imagine we're using "django-celery-results" extension for storing
# # Task results in DB

# CELERY_RESULT_BACKEND  = "django-db"
# CELERY_RESULT_EXTENDED = True









