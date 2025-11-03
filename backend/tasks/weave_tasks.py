from tasks.celery import celery_app
import algorithm.main
from utils.storages import LocalFileStorage
import os
import asyncio

storage = LocalFileStorage()


@celery_app.task(bind=True)
async def weave_image(image_path, board_path, name):
    # result_path = algorithm.main.weave_image(image_path, board_path, name)
    try:
        await asyncio.sleep(3)
        image = await storage.read(image_path)
        if image:
            return "zoo wee mama"
    except IOError as e:
        return f"Error reading image: {str(e)}"
