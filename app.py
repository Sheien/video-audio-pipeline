from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import whisper
import uuid
import httpx
import os

app = FastAPI()

# Folders (optional, create them)
os.makedirs("downloads", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)

XANO_UPLOAD_URL = "https://your-xano-url/upload"
XANO_SUMMARY_URL = "https://your-xano-url/video_summary"

class DownloadRequest(BaseModel):
    url: str

@app.get("/")
def root():
    return {"message": "✅ Server is running!"}

@app.post("/download")
def download_video(data: DownloadRequest):
    try:
        video_id = str(uuid.uuid4())
        filepath = f"downloads/{video_id}.mp4"
        cmd = ["yt-dlp", "-o", filepath, data.url]
        subprocess.run(cmd, check=True)
        return {"status": "downloaded", "file": filepath, "id": video_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe/{video_id}")
def transcribe_video(video_id: str):
    filepath = f"downloads/{video_id}.mp4"
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Video file not found.")

    model = whisper.load_model("base")
    result = model.transcribe(filepath)
    transcript = result["text"]

    # Save to file (optional)
    with open(f"transcripts/{video_id}.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    # Send to Xano
    try:
        httpx.post(XANO_UPLOAD_URL, json={
            "filename": f"{video_id}.mp4",
            "url": f"/downloads/{video_id}.mp4"
        })
        httpx.post(XANO_SUMMARY_URL, json={
            "video_id": video_id,
            "summary": transcript
        })
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Xano error: {str(e)}")

    return {"status": "transcribed", "text": transcript}
