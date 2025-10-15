from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from tasks import process_image
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/process")
async def process(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    task = process_image.delay(file_path)
    return {"task_id": task.id}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task = process_image.AsyncResult(task_id)
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
    task = process_image.AsyncResult(task_id)
    if task.state == "SUCCESS":
        return FileResponse(task.result["video_path"], media_type="video/mp4")
    return {"error": "Not ready"}
