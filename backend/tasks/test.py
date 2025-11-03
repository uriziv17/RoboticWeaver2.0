from tasks.celery import celery_app
import time

@celery_app.task(bind=True)
def dummy_task(self, duration):
    total = 100
    for i in range(total):
        time.sleep(duration / total)
        self.update_state(state='PROGRESS', meta={'progress': i + 1})
    return {'progress': 100}
