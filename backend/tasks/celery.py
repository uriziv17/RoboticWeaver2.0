import os
from celery import Celery
from time import sleep


BROKER = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", BROKER)

celery = Celery("tasks", broker=BROKER, backend=RESULT_BACKEND)

@celery.task(bind=True)
def dummy_task(self, duration):
    total = 100
    for i in range(total):
        sleep(duration / total)
        self.update_state(state='PROGRESS', meta={'progress': i + 1})
    return {'progress': 100}
