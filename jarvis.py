import sounddevice as sd
import numpy as np
import time
import speech_recognition as sr
import subprocess

CLAP_THRESHOLD = 0.6
CLAP_GAP = 0.7
SAMPLE_RATE = 44100
COOLDOWN = 3
BLOCK_SIZE = 256

clap_times = []
listening = True
last_trigger_time = 0

last_clap_time = 0
MIN_CLAP_INTERVAL = 0.15  # Reduced from 0.3 for faster detection

def detect_clap(indata):
    global last_clap_time, clap_times, listening, last_trigger_time

    volume = np.linalg.norm(indata)
    peak = np.max(np.abs(indata))
    now = time.time()

    if peak > 0.02 and volume < 0.18:
        if now - last_clap_time > MIN_CLAP_INTERVAL:
            last_clap_time = now

            clap_times = [t for t in clap_times if now - t < 1.0]
            clap_times.append(now)

            print(f"Clap detected (peak: {peak:.4f}, vol: {volume:.4f})")

            if len(clap_times) >= 2:
                if clap_times[-1] - clap_times[-2] <= CLAP_GAP:
                    if time.time() - last_trigger_time >= COOLDOWN and listening:
                        print("Double clap confirmed")
                        clap_times.clear()
                        last_trigger_time = time.time()
                        listening = False
                        activate_voice_mode()
                        listening = True


def listen_for_claps():
    global listening, last_trigger_time
    print("Listening for claps...")
    with sd.InputStream(
        callback=lambda indata, frames, t, status: detect_clap(indata),
        channels=1,
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        latency='low'
    ):
        while True:
            time.sleep(0.05)  # Reduced from 0.1 to improve responsiveness

            if not listening:
                continue

            if time.time() - last_trigger_time < COOLDOWN:
                continue

            if len(clap_times) == 2:
                if clap_times[1] - clap_times[0] <= CLAP_GAP:
                    print("Double clap confirmed")
                    clap_times.clear()
                    last_trigger_time = time.time()
                    listening = False
                    activate_voice_mode()
                    listening = True
                    
def activate_voice_mode():
    print("Say: let's get it started")
    r = sr.Recognizer()
    r.energy_threshold = 4000
    r.dynamic_energy_threshold = False

    try:
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        
        print("Processing...")
        text = r.recognize_google(audio).lower()
        print("You said:", text)

        if "let's get it started" in text or "get it started" in text or "go" in text:
            launch_dev_env()
        else:
            print("Command not recognized. Try 'let's get it started' or 'go'")

    except sr.UnknownValueError:
        print("Couldn't understand your speech")
    except sr.RequestError as e:
        print("Speech service error:", e)
    except sr.Timeout:
        print("No speech detected (timeout)")

def launch_dev_env():
    print("Launching dev environment")
    subprocess.run(["open", "-a", "safari"])
    subprocess.run(["open", "-a", "Terminal"])

if __name__ == "__main__":
    listen_for_claps()
