"""import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

q = queue.Queue()

model = Model("model")
recognizer = KaldiRecognizer(model, 16000)

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("Listening...")

        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                if text:
                    print("You:", text)
                    return text"""
                    
"""import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

q = queue.Queue()
model = Model("model")
recognizer = KaldiRecognizer(model, 16000)

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen():
    print("Listening...")

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback
    ):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                
                if text:
                    print("You:", text)
                    break   # EXIT LOOP IMMEDIATELY

    return text  # return AFTER stream closes"""

import os
import queue
import tempfile
import wave

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
BLOCK_SIZE = 1024
MAX_SECONDS = 12
SILENCE_SECONDS = 1.0
SILENCE_THRESHOLD = 350

# First run downloads the model automatically.
# Start with base.en. If your laptop feels slow, change to tiny.
MODEL_NAME = "base.en"
model = WhisperModel(MODEL_NAME, device="cpu", compute_type="int8")


def _record_utterance():
    audio_queue = queue.Queue()
    frames = []
    speech_started = False
    silence_chunks = 0
    max_chunks = int(MAX_SECONDS * SAMPLE_RATE / BLOCK_SIZE)
    silence_limit = int(SILENCE_SECONDS * SAMPLE_RATE / BLOCK_SIZE)

    def callback(indata, frame_count, time_info, status):
        if status:
            print(status)
        audio_queue.put(bytes(indata))

    print("Listening...")

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        for _ in range(max_chunks):
            chunk = audio_queue.get()
            data = np.frombuffer(chunk, dtype=np.int16)

            if data.size == 0:
                continue

            rms = float(np.sqrt(np.mean(data.astype(np.float32) ** 2)))

            if rms > SILENCE_THRESHOLD:
                speech_started = True
                silence_chunks = 0
                frames.append(chunk)
            elif speech_started:
                frames.append(chunk)
                silence_chunks += 1
                if silence_chunks >= silence_limit:
                    break

    return b"".join(frames)


def listen():
    audio_bytes = _record_utterance()
    if not audio_bytes:
        return ""

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            temp_path = tmp.name

        with wave.open(temp_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_bytes)

        segments, info = model.transcribe(
            temp_path,
            beam_size=1,
            vad_filter=True,
            language="en",
        )

        text = " ".join(segment.text.strip() for segment in segments).strip()
        if text:
            print("You:", text)
        return text

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)