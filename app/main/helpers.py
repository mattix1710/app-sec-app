import time
from celery import shared_task

@shared_task
def really_long_wait():
    print("START SLEEP")
    time.sleep(5.0)
    print("STOP SLEEP")