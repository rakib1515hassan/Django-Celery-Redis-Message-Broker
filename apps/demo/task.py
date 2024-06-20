# from config.celery import app
from celery import shared_task
from celery.result import AsyncResult

from time import sleep


def test_1(x, y):
    sleep(10)          ##! 10 seconds delay করা হয়ছে For testing
    result = x + y
    return result



# @app.task
@shared_task(name="Two number add")   ##? এখানে shared_task এবং app.task একি কাজ করে, But আমাদের shared_task ব্যবহার করবো।
def add(x, y):
    sleep(10)          ##! 20 seconds delay করা হয়ছে For testing
    result = x + y
    return result



@shared_task   
def sub(x, y):
    sleep(10)          ##! 10 seconds delay করা হয়ছে For testing
    result = x - y
    return result


@shared_task   
def add_result(task_id):
    result = AsyncResult(task_id)
    return result




##? প্রতি ৫ সেকেন্ড পর পর প্রথম সংখ্যার সাথে একটি নির্দিষ্ট সংখ্যা যোগ করতে থাকবে এবং এই প্রক্রিয়া চালিয়ে যাবে যতক্ষণ পর্যন্ত আপনি এটি বন্ধ না করেন।
@shared_task(bind=True)
def add_periodically(self, initial_value, increment_value, max_iterations):
    current_value = initial_value
    for _ in range(max_iterations):
        current_value += increment_value
        print(f'Current Value: {current_value}')
        sleep(5)
    return current_value







##? আপনি যদি সেলারি ব্যবহার করে একটি নির্দিষ্ট সময় পরপর (যেমন, প্রতি ১০ সেকেন্ড) আপনার সেশন ক্যাশ পরিষ্কার করতে চান,
from django.contrib.sessions.models import Session
import logging

logger = logging.getLogger(__name__)

@shared_task
def clear_session_cache():
    logger.info("Clearing session cache...")
    try:
        Session.objects.all().delete()
        logger.info("Session cache cleared successfully.")
    except Exception as e:
        logger.error(f"Error clearing session cache: {e}")





##? প্রতি ১ মিনিট পর পর task_backend টেবিলে যে ডেটা আছে তা মুছে ফেলার জন্য একটি সেলারি টাস্ক তৈরি করা এবং Celery Beat এর মাধ্যমে সেটিকে শিডিউল করা খুব সহজ। এই প্রক্রিয়াটির জন্য আপনাকে সেলারি ও সেলারি বিট কনফিগার করতে হবে, এবং একটি টাস্ক তৈরি করতে হবে যা এই কাজটি করবে।
from django_celery_results.models import TaskResult

@shared_task
def clear_task_backend_data():
    logger.info("Clearing task backend data...")
    try:
        TaskResult.objects.all().delete()
        logger.info("Task backend data cleared successfully.")
    except Exception as e:
        logger.error(f"Error clearing task backend data: {e}")





@shared_task
def Test_Notification_Send(id):
    print(f"Test Notification Send: {id}")
    return id