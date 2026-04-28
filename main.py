# main.py
import base64
import json
import os
import uuid
from io import BytesIO
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, Form
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# TTS
from gtts import gTTS

# STT (Vosk)
import wave
import numpy as np
from vosk import Model, KaldiRecognizer, SetLogLevel

SetLogLevel(-1)  # silence Vosk logs (optional)

app = FastAPI()

# Allow CORS for local development — remove or restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to Vosk model directory — change to where you installed the model
VOSK_MODEL_PATH = "model"  # put the unziped Vosk model here

if not os.path.exists(VOSK_MODEL_PATH):
    print("WARNING: Vosk model not found at:", VOSK_MODEL_PATH)
    print("Download a model (e.g., small model) and extract to the 'model' folder.")
else:
    model = Model(VOSK_MODEL_PATH)


@app.websocket("/ws/stt")
async def websocket_stt(ws: WebSocket):
    """
    WebSocket STT endpoint.

    Protocol (JSON messages):
    - Client sends audio chunks encoded as base64 with {"type":"audio","data":"<base64 pcm16>"}
    - Client sends {"type":"start","sample_rate":16000} to init
    - Client sends {"type":"end"} when done; server will send final result and close optionally.
    - Server pushes {"type":"partial","text":"..."} and {"type":"final","text":"..."} messages.
    """
    await ws.accept()
    rec = None
    sample_rate = 16000  # default
    try:
        while True:
            msg = await ws.receive_text()
            payload = json.loads(msg)

            if payload.get("type") == "start":
                sample_rate = int(payload.get("sample_rate", sample_rate))
                if 'model' not in globals():
                    await ws.send_text(json.dumps({"type": "error", "message": "Vosk model not loaded on server."}))
                    continue
                rec = KaldiRecognizer(model, sample_rate)
                rec.SetWords(True)
                await ws.send_text(json.dumps({"type": "started"}))

            elif payload.get("type") == "audio":
                if rec is None:
                    await ws.send_text(json.dumps({"type":"error","message":"Recognizer not initialized. Send a start message first."}))
                    continue
                b64 = payload.get("data")
                audio_bytes = base64.b64decode(b64)

                # Feed to recognizer; Vosk expects PCM 16-bit mono
                if rec.AcceptWaveform(audio_bytes):
                    res = json.loads(rec.Result())
                    text = res.get("text", "")
                    await ws.send_text(json.dumps({"type": "final", "text": text}))
                else:
                    partial = json.loads(rec.PartialResult())
                    ptext = partial.get("partial", "")
                    await ws.send_text(json.dumps({"type": "partial", "text": ptext}))

            elif payload.get("type") == "end":
                if rec is None:
                    await ws.send_text(json.dumps({"type":"error","message":"No active recognizer."}))
                    continue
                final = json.loads(rec.FinalResult())
                text = final.get("text", "")
                await ws.send_text(json.dumps({"type": "final", "text": text}))
                await ws.send_text(json.dumps({"type": "ended"}))
                # keep connection open if you want; client may close
    except WebSocketDisconnect:
        print("WebSocket disconnected")


@app.post("/tts")
async def tts_endpoint(text: str = Form(...), lang: str = Form("en"), slow: Optional[bool] = Form(False)):
    """
    Simple TTS: generate MP3 for the given text and return it as streaming response.
    Example (curl):
      curl -X POST -F "text=hello world" http://localhost:8000/tts --output out.mp3
    """
    if not text:
        return JSONResponse({"error": "text is required"}, status_code=400)
    try:
        tts = gTTS(text=text, lang=lang, slow=slow)
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        headers = {
            "Content-Disposition": f'attachment; filename="tts-{uuid.uuid4().hex[:8]}.mp3"'
        }
        return StreamingResponse(buf, media_type="audio/mpeg", headers=headers)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# Optional: health check
@app.get("/health")
async def health():
    return {"status": "ok"}
from fastapi.responses import HTMLResponse

@app.get("/")
async def homepage():
    with open("index.html", "r") as f:
        return HTMLResponse(f.read())
