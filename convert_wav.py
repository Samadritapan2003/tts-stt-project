from pydub import AudioSegment

audio = AudioSegment.from_wav("sample.wav")

# convert to mono 16k PCM WAV
audio = audio.set_channels(1)
audio = audio.set_frame_rate(16000)

audio.export("fixed.wav", format="wav")
print("Converted successfully → fixed.wav")
