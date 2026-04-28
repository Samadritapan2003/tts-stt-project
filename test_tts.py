from gtts import gTTS

print("\n======================")
print("       TTS DEMO")
print("======================\n")

text_input = "HELLO CHECKING FOR TEXT TO SPEECH"

print("TEXT GIVEN:")
print(text_input + "\n")

tts = gTTS(text_input)
tts.save("presentation_tts.mp3")

print("SPEECH SAID:")
print(text_input)
