from typing import Optional
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from tasks.test import dummy_task
from tasks.weave_tasks import weave_image
import shutil
import os
from pydantic import BaseModel
from backend.utils.storages import LocalFileStorage

app = FastAPI()

storage = LocalFileStorage()


class DurationRequest(BaseModel):
    duration: int


@app.post("/dummy/")
def dummy(payload: DurationRequest):
    task = dummy_task.delay(payload.duration)
    return {"task_id": task.id}


@app.post("/process")
async def process(file: UploadFile = File(...)):
    await storage.save(file.filename, await file.read())
    task = weave_image.delay(file.filename)
    return {"task_id": task.id}


# @app.get("/status/{task_id}")
# async def get_status(task_id: str):
#     task = process_image.AsyncResult(task_id)
#     if task.state == "PENDING":
#         return {"status": "pending"}
#     elif task.state == "PROGRESS":
#         return {"status": "processing", "progress": task.info.get("progress", 0)}
#     elif task.state == "SUCCESS":
#         return {"status": "done", "result": task.result}
#     else:
#         return {"status": task.state.lower()}

# @app.get("/result/{task_id}")
# async def get_result(task_id: str):
#     task = process_image.AsyncResult(task_id)
#     if task.state == "SUCCESS":
#         return FileResponse(task.result["video_path"], media_type="video/mp4")
#     return {"error": "Not ready"}
