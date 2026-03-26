from voice_recognizer import VoiceController
import pyautogui
import time
import pygetwindow as gw
import os
import sys
import ctypes
import vosk

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def next_slide():
    print(">>> ACTION: Next slide")
    windows = gw.getWindowsWithTitle('PowerPoint') 
    if windows:
        win = windows[0]
        win.activate()
        pyautogui.press('down')
    else:
        print("Presentation window not found!")

def previous_slide():
    print(">>> ACTION: Previous Slide")
    windows = [w for w in gw.getAllWindows() if 'powerpoint' in w.title.lower()]
    if windows:
        win = windows[0]
        win.activate()
        pyautogui.press('up')
    else:
        print("Presentation window not found!")


COMMAND_MAP = {
    "pilot next": next_slide,
    "pilot previous": previous_slide,
}

def handle_voice_command(text):
    """This function runs whenever Vosk hears a valid word."""
    print(f"Heard: {text}")
    
    if text in COMMAND_MAP:
        COMMAND_MAP[text]()
    else:
        print("Command recognized but no action assigned.")

if __name__ == "__main__":
    vosk.SetLogLevel(-1)
    ctypes.windll.kernel32.SetConsoleTitleW("Pilot v1.0 | Active Listening")
    vocab = list(COMMAND_MAP.keys()) + ["[unk]"]
    
    vc = VoiceController(model_path=resource_path("model"), vocabulary=vocab, on_command_detected=handle_voice_command)
    print("--- Pilot v1.0 Started ---")
    vc.start()

    try:
        print("Pilot Listening...")
        print('Say "pilot next" for next slide')
        print('Say "pilot previous" for previous slide')
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        vc.stop()
