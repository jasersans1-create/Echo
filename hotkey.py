from pynput import keyboard
import subprocess
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_jarvis():
    subprocess.Popen([
        sys.executable,
        os.path.join(BASE_DIR, "main.py"),
        "--model",
        os.path.join(BASE_DIR, "models", "vosk-model-small-en-us-0.15"),
    ], cwd=BASE_DIR)

print("Jarvis background mode started")
print("Press Ctrl+Space")

current = set()

def on_press(key):
    current.add(key)
    if keyboard.Key.ctrl_l in current and keyboard.Key.space in current:
        run_jarvis()

def on_release(key):
    current.discard(key)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
