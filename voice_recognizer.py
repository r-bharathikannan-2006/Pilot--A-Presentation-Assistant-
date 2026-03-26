import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import threading

class VoiceController:
    def __init__(self, model_path, vocabulary, on_command_detected):
        self.model = Model(model_path)
        self.vocabulary = vocabulary
        self.on_command_detected = on_command_detected
        self.running = False
        self.q = queue.Queue()

    def _audio_callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def start(self):
        self.running = True
        threading.Thread(target=self._listen, daemon=True).start()

    def _listen(self):
        rec = KaldiRecognizer(self.model, 16000, json.dumps(self.vocabulary))
        
        with sd.RawInputStream(samplerate=16000, blocksize=2000, 
                               dtype='int16', channels=1, 
                               callback=self._audio_callback):
            while self.running:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    rec.Result() 
                else:
                    partial = json.loads(rec.PartialResult())
                    text = partial.get("partial", "").strip()
                    
                    if text in self.vocabulary and text != "[unk]":
                        self.on_command_detected(text)
                        rec.Reset()

    def stop(self):
        self.running = False