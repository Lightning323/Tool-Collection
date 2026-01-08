import tkinter as tk
from tkinter import ttk
import numpy as np
import random

class RecorderUI:
    def __init__(self, root):
        root.title("Super Classroom Recorder 3000")

        self.is_recording = False

        # ---- Main Container ----
        main = ttk.Frame(root, padding=15)
        main.pack(fill="both", expand=True)

        # ---- Controls Row ----
        controls = ttk.Frame(main)
        controls.pack(fill="x", pady=(0, 10))

        self.start_btn = ttk.Button(controls, text="Start Recording", command=self.start_recording)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = ttk.Button(controls, text="Stop Recording", command=self.stop_recording)
        self.stop_btn.grid(row=0, column=1, padx=5)

        # ---- Waveform Display ----
        waveform_frame = ttk.LabelFrame(main, text="Waveform", padding=10)
        waveform_frame.pack(fill="x", expand=False, pady=(0, 10))

        self.waveform_canvas = tk.Canvas(
            waveform_frame,
            height=100,
            background="#111",
            highlightthickness=0
        )
        self.waveform_canvas.pack(fill="both", expand=True)

        # Store waveform line
        self.waveform_line = None

        # ---- Transcription Area ----
        transcription_frame = ttk.LabelFrame(main, text="Transcription", padding=10)
        transcription_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.transcription_box = tk.Text(
            transcription_frame,
            wrap="word",
            height=6
        )
        self.transcription_box.pack(fill="both", expand=True)

        # ---- Save Buttons ----
        save_row = ttk.Frame(main)
        save_row.pack(fill="x")

        self.save_audio_btn = ttk.Button(save_row, text="Save Audio")
        self.save_audio_btn.grid(row=0, column=0, padx=5)

        self.save_transcription_btn = ttk.Button(save_row, text="Save Transcription")
        self.save_transcription_btn.grid(row=0, column=1, padx=5)

        # Kick off waveform updater
        root.after(30, self.update_waveform)


    # -----------------------------
    # Fake waveform logic
    # -----------------------------
    def start_recording(self):
        self.is_recording = True

    def stop_recording(self):
        self.is_recording = False

    def update_waveform(self):
        """Draws fake random noise as the waveform while recording."""
        self.waveform_canvas.delete("wave")

        w = self.waveform_canvas.winfo_width()
        h = self.waveform_canvas.winfo_height()

        if w < 10 or h < 10:
            # Canvas hasn't fully rendered yet — try again shortly
            self.waveform_canvas.after(30, self.update_waveform)
            return

        # Generate wiggles if recording
        if self.is_recording:
            points = []
            for x in range(0, w, 4):  # step size = fewer points for speed
                y = h/2 + random.uniform(-1, 1) * (h/3)
                points.extend([x, y])

            self.waveform_canvas.create_line(
                points,
                fill="#00ff77",
                width=2,
                smooth=True,
                tags="wave"
            )

        # Loop forever in a polite, scheduled, well-behaved way
        self.waveform_canvas.after(30, self.update_waveform)


if __name__ == "__main__":
    root = tk.Tk()
    app = RecorderUI(root)
    root.mainloop()
