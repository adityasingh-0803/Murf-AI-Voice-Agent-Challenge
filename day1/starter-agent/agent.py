import os
import pyaudio
import wave
import requests
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")

openai.api_key = OPENAI_API_KEY

AUDIO_FILE = "input.wav"

# -----------------------------
# RECORD AUDIO (5 seconds)
# -----------------------------
def record_audio():
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 16000
    seconds = 5

    p = pyaudio.PyAudio()
    print("🎤 Recording...")

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []
    for _ in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(AUDIO_FILE, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("🎤 Recording Complete")

# -----------------------------
# SPEECH → TEXT (Whisper)
# -----------------------------
def transcribe_audio():
    print("📝 Transcribing...")
    audio_file = open(AUDIO_FILE, "rb")
    
    transcript = openai.audio.transcriptions.create(
        model="gpt-4o-mini-tts",
        file=audio_file
    )

    text = transcript.text
    print("🗣 You said:", text)
    return text

# -----------------------------
# TEXT → RESPONSE (GPT)
# -----------------------------
def generate_response(prompt):
    print("🤖 Generating response...")
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = completion.choices[0].message['content']
    print("🤖 Agent:", reply)
    return reply

# -----------------------------
# TEXT → SPEECH (Murf Falcon)
# -----------------------------
def speak_with_murf(text):
    print("🎧 Converting to speech using Murf Falcon...")

    url = "https://api.murf.ai/v1/speech/generate"

    headers = {
        "accept": "audio/mpeg",
        "Content-Type": "application/json",
        "api-key": MURF_API_KEY,
    }

    payload = {
        "voiceId": "falcon",
        "text": text,
        "format": "mp3"
    }

    response = requests.post(url, json=payload, headers=headers)

    out_file = "response.mp3"
    with open(out_file, "wb") as f:
        f.write(response.content)

    print("🔊 Playing response...")

    os.system("start response.mp3" if os.name == "nt" else "mpg123 response.mp3")

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    record_audio()
    text = transcribe_audio()
    reply = generate_response(text)
    speak_with_murf(reply)
