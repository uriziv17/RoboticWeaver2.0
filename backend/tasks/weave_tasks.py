import time
from tasks.celery import celery_app
import algorithm.main
from utils.storages import SyncFileStorage
import os

storage = SyncFileStorage()


@celery_app.task(bind=True)
def weave_image(self, image_path):
    # result_path = algorithm.main.weave_image(image_path, board_path, name)
    try:
        time.sleep(20)
        image = storage.read(image_path)
        if image:
            return "zoo wee mama"
    except IOError as e:
        return f"Error reading image: {str(e)}"
