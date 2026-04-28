import requests
import base64
import asyncio
import websockets
import json
from pydub import AudioSegment

# --- TTS Test ---
tts_url = "http://127.0.0.1:8000/tts"
tts_data = {"text": "Hello world from Samadrita!"}

print("Testing TTS endpoint...")
resp = requests.post(tts_url, data=tts_data)
if resp.status_code == 200:
    with open("test_output.mp3", "wb") as f:
        f.write(resp.content)
    print("TTS successful! Audio saved as test_output.mp3")
else:
    print("TTS failed:", resp.text)

# --- Convert MP3 to WAV (16kHz mono) ---
sound = AudioSegment.from_file("test_output.mp3", format="mp3")
sound = sound.set_channels(1).set_frame_rate(16000)
sound.export("sample.wav", format="wav")
print("Converted TTS MP3 → PCM16 WAV as sample.wav")

# --- STT Test ---
async def test_stt():
    uri = "ws://127.0.0.1:8000/ws/stt"
    async with websockets.connect(uri) as ws:
        print("Testing STT endpoint...")
        await ws.send(json.dumps({"type": "start", "sample_rate": 16000}))

        with open("sample.wav", "rb") as f:
            chunk = f.read(4000)  # send in small chunks
            while chunk:
                await ws.send(json.dumps({"type": "audio", "data": base64.b64encode(chunk).decode()}))
                chunk = f.read(4000)

        await ws.send(json.dumps({"type": "end"}))

        while True:
            try:
                msg = await ws.recv()
                print(msg)
                data = json.loads(msg)
                if data.get("type") == "ended":
                    break
            except websockets.ConnectionClosed:
                break

asyncio.run(test_stt())
