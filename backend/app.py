from typing import Optional
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from tasks.test import dummy_task
from tasks.weave_tasks import weave_image
import shutil
import os
from pydantic import BaseModel
from utils.storages import AsyncFileStorage

app = FastAPI()

storage = AsyncFileStorage()


class DurationRequest(BaseModel):
    duration: int


@app.post("/dummy/")
def dummy(payload: DurationRequest):
    task = dummy_task.delay(payload.duration)
    return {"task_id": task.id}


@app.post("/process")
async def process(file: UploadFile = File(...)):
    file_path = await storage.save(file.filename, await file.read())
    task = weave_image.delay(file_path)
    return {"task_id": task.id}


@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task = weave_image.AsyncResult(task_id)
    if task.state == "PENDING":
        return {"status": "pending"}
    elif task.state == "PROGRESS":
        return {"status": "processing", "progress": task.info.get("progress", 0)}
    elif task.state == "SUCCESS":
        return {"status": "done", "result": task.result}
    else:
        return {"status": task.state.lower()}

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task = weave_image.AsyncResult(task_id)
    if task.state == "SUCCESS":
        return FileResponse(task.result, media_type="image/png")
    return {"error": "Not ready"}
