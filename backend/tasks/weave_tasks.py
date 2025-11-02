from celery_app import celery_app
import algorithm.main

@celery_app.task(bind=True)
def weave_image(image_path, board_path, name):
    result_path = algorithm.main.weave_image(image_path, board_path, name)
    return result_path