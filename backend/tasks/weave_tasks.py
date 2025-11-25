import time
from tasks.celery import celery_app
import algorithm.main
from utils.storages import SyncFileStorage
import os

storage = SyncFileStorage()


@celery_app.task(bind=True)
def weave_image(self, image_path):
    board_path = "./algorithm/Images/board_circle.png"
    try:
        result_path = algorithm.main.weave_image(image_path, board_path, id=self.request.id)
        return result_path
    except IOError as e:
        return f"Error reading image: {str(e)}"
