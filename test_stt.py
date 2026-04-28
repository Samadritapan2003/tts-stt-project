from vosk import Model, KaldiRecognizer
import sys
import wave
import json

print("\n======================")
print("       STT DEMO")
print("======================\n")

# Initialize
wf = wave.open("sample_fixed.wav", "rb")
model = Model("model")
rec = KaldiRecognizer(model, wf.getframerate())

# Print the expected input
print("INPUT FROM VOICE:")
print("HELLO TESTING TESTING THING\n")  # <-- write what your sample.wav contains

print("VOICE TO TEXT:")

# Run STT
result_text = ""
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())
        result_text += res.get("text", "")
res = json.loads(rec.FinalResult())
result_text += res.get("text", "")

# Print recognized text
print(result_text.upper())
