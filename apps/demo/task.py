# from config.celery import app
from celery import shared_task
from celery.result import AsyncResult

from time import sleep


def test_1(x, y):
    sleep(10)          ##! 10 seconds delay করা হয়ছে For testing
    result = x + y
    return result



# @app.task
@shared_task   ##? এখানে shared_task এবং app.task একি কাজ করে, But আমাদের shared_task ব্যবহার করবো।
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