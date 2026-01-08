import os
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import whisper
import sounddevice as sd
import numpy as np
from collections import deque
import tempfile
from scipy.io.wavfile import write
import ipywidgets as widgets
from IPython.display import display, clear_output
import threading

"""
pip install openai-whisper
pip install sounddevice
pip install scipy
pip install numpy
pip install torch
pip install ipywidgets
"""


# ----- PARAMETERS -----
samplerate = 8000
channels = 1
chunk_sec = 1      # 1 second per chunk
window_sec = 5     # rolling window for live preview
final_audio_path = "final_audio.wav"
final_transcript_path = "final_transcript.txt"

save_path = "C:\\Users\\sampw\\OneDrive\\Code Projects\\Python\\Projects\\Multi Tool\\AudioTranscription\\out"
final_audio_path = os.path.join(save_path, "final-audio.wav")
final_transcript_path = os.path.join(save_path, "final-transcript.txt")

print("Loading Whisper model...")
model = whisper.load_model("medium")#medium
print("Model loaded!")


# ----- STATE -----
rolling = deque(maxlen=samplerate * window_sec)
full_audio = []


# ----- HELPER -----
def timestamp():
    return datetime.now().strftime("%H:%M:%S")

print("Recording audio. Press Ctrl+C to stop.")
while True:
    try:
        chunk = sd.rec(int(chunk_sec * samplerate),
                        samplerate=samplerate,
                        channels=channels)
        sd.wait()
        
        full_audio.append(chunk.copy())
        rolling.extend(chunk.flatten())
        
        # ----- LIVE PREVIEW -----
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        window_audio = np.array(rolling, dtype=np.float32)
        write(tmp.name, samplerate, window_audio)

        print("Transcribing live preview (this may take a moment)...")

        preview = model.transcribe(tmp.name, task="transcribe")  # replace as needed
        tmp.close()
        os.remove(tmp.name)

        # Update GUI and print timestamped line
        text = preview['text'].strip()
        print("TEXT:", text)
        if text:
            print(f"[{timestamp()}] {text}")
    except KeyboardInterrupt:
        break

# ----- SAVE FINAL AUDIO & TRANSCRIPT -----
full_array = np.concatenate(full_audio).astype(np.float32)
write(final_audio_path, samplerate, full_array)
print(f"[{timestamp()}] 💾 Saved full audio: {final_audio_path}")
message.value = f"💾 Saved full audio: {final_audio_path}"

message.value = "📝 Transcribing full audio (this may take a moment)…"
result = model.transcribe(final_audio_path, task="translate")
with open(final_transcript_path, "w", encoding="utf-8") as f:
    f.write(result["text"])
print(f"[{timestamp()}] ✨ Final transcript saved: {final_transcript_path}")
message.value = f"✨ Final transcript saved: {final_transcript_path}"
