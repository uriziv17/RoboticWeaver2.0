from celery_app import celery_app
import algorithm.main
from backend.utils.storages import LocalFileStorage
import os

storage = LocalFileStorage()


@celery_app.task(bind=True)
async def weave_image(image_path, board_path, name):
    # result_path = algorithm.main.weave_image(image_path, board_path, name)
    try:
        image = await storage.read(image_path)
        if image:
            return "zoo wee mama"
    except IOError as e:
        return f"Error reading image: {str(e)}"
