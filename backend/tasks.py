from celery import Celery
from time import sleep
import uuid
import os

app = Celery("tasks")
app.config_from_object("celeryconfig")

OUTPUT_DIR = "videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.task(bind=True)
def process_image(self, image_path):
    # Simulate slow computation
    for i in range(10):
        sleep(6)  # total ~60s
        self.update_state(state="PROGRESS", meta={"progress": (i+1)*10})

    # Instead of real CV, just save a "fake video file"
    job_id = str(uuid.uuid4())
    video_path = os.path.join(OUTPUT_DIR, f"{job_id}.mp4")
    with open(video_path, "wb") as f:
        f.write(b"FAKE VIDEO CONTENT")

    return {"video_path": video_path}
