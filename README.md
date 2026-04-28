# 🎙️ STT ↔ TTS Engine (Real-Time Speech Pipeline)

This module handles **Speech-to-Text (STT)** and **Text-to-Speech (TTS)** processing for our real-time video meeting application.

It enables seamless voice input → text output and text input → spoken audio output.

---

## 🚀 Features

### 🎤 Speech-to-Text (STT)

* Integrated **Vosk offline acoustic model**
* 16kHz mono audio processing
* WAV file handling
* Real-time chunk processing using `recognizer.AcceptWaveform`
* Converts speech → text output
* Terminal-based working prototype

### 🔊 Text-to-Speech (TTS)

* Integrated **gTTS (Google Text-to-Speech)**
* Implemented **pyttsx3 fallback** for offline support
* Converts text → MP3 / spoken output
* Automatic audio playback
* Standalone working endpoint / script

### 🔁 Audio Processing Pipeline

* Text → Speech
* Speech → Text
* Audio preprocessing handled (resampling + formatting)
* Functional backend logic ready for integration

---

## 🏗️ Project Structure

```
tts_project/
│
├── stt.py
├── tts.py
├── model/               # Vosk acoustic model
├── audio_samples/
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/YOUR_USERNAME/stt-tts-engine.git
cd stt-tts-engine
```

### 2️⃣ Create virtual environment (recommended)

```
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ Running Speech-to-Text

```
python stt.py
```

Provide a 16kHz mono WAV file as input.

Output:

```
Recognized Text: hello everyone welcome to the meeting
```

---

## ▶️ Running Text-to-Speech

```
python tts.py
```

Input text is converted to speech and played automatically.

---

## 🔄 Current Status

| Module                | Status         |
| --------------------- | -------------- |
| Basic STT             | ✅ Working      |
| Basic TTS             | ✅ Working      |
| Audio Preprocessing   | ✅ Working      |
| Terminal Demo         | ✅ Complete     |
| Real-Time Streaming   | 🟡 In Progress |
| WebSocket Integration | 🔜 Planned     |

---

## 🎯 Next Phase (Integration Plan)

* Implement WebSocket streaming for live audio chunks
* Connect STT output directly to frontend overlay
* Auto-trigger TTS from gesture prediction module
* Add async concurrency for multiple participants
* Optimize latency and model loading

---

## 👩‍💻 Role in Group Project

This module is responsible for:

* Real-time speech recognition
* Speech synthesis
* Audio pipeline handling
* Backend voice processing logic

---

## 🧠 Tech Stack

* Python
* Vosk
* gTTS
* pyttsx3
* WebSocket (planned)
* FastAPI / Flask (integration phase)

---

## 📌 Note

This is currently a **functional prototype**.
The next milestone is full real-time streaming integration with the video meeting frontend.

---

Built with focus on real-time accessibility and communication enhancement.
