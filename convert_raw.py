import soundfile as sf

data, samplerate = sf.read("sample.wav")
sf.write("fixed.wav", data, samplerate)
print("Re-saved WAV!")
