# test_api_wav.py
import asyncio
import base64
import json
import requests
import websockets

# ---- TTS Test ----
tts_url = "http://127.0.0.1:8000/tts"
tts_data = {"text": "Hello, this is a test for TTS!"}

print("Testing TTS endpoint...")
resp = requests.post(tts_url, data=tts_data)
if resp.status_code == 200:
    with open("tts_output.mp3", "wb") as f:
        f.write(resp.content)
    print("TTS successful! Audio saved as tts_output.mp3")
else:
    print("TTS failed:", resp.text)

# ---- STT Test ----
async def test_stt():
    ws_url = "ws://127.0.0.1:8000/ws/stt"
    wav_path = "sample.wav"  # <-- must be WAV PCM16 mono

    async with websockets.connect(ws_url) as ws:
        # Start message
        await ws.send(json.dumps({"type": "start", "sample_rate": 16000}))
        print(await ws.recv())  # {"type": "started"}

        # Send audio
        with open(wav_path, "rb") as f:
            audio_bytes = f.read()
        await ws.send(json.dumps({
            "type": "audio",
            "data": base64.b64encode(audio_bytes).decode("utf-8")
        }))

        # End message
        await ws.send(json.dumps({"type": "end"}))

        while True:
            try:
                msg = await ws.recv()
                print(msg)
                if json.loads(msg).get("type") == "ended":
                    break
            except:
                break

print("\nTesting STT endpoint...")
asyncio.run(test_stt())
