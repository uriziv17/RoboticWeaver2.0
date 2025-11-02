import os
from celery import Celery


BROKER = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", BROKER)

celery_app = Celery("tasks", broker=BROKER, backend=RESULT_BACKEND)
