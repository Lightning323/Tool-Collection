import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, ttk
import colorsys
import sys
from PIL import Image
import os


class GPLPaletteManager:
    def __init__(self, root):
        self.root = root
        self.root.title("GPL Palette Manager")

        # Internal palette storage: list of tuples (R,G,B)
        self.palette = set()  # Use a set to guarantee unique colors

        # Label for color count
        self.color_label = tk.Label(root, text="Colors in palette: 0")
        self.color_label.pack(pady=5)

        # Scrollable canvas for grid of colors
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame, bg="white", height=300)
        self.scrollbar = tk.Scrollbar(
            self.frame, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Inner frame to hold color rectangles
        self.inner_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", lambda e: self.draw_palette())

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        columnCounter = 0
        tk.Button(btn_frame, text="Import GPL", command=self.load_gpl).grid(
            row=0, column=columnCounter, padx=5
        )
        columnCounter += 1
        tk.Button(
            btn_frame, text="Import Hex File (.txt)", command=self.import_hex_file
        ).grid(row=0, column=columnCounter, padx=5)
        columnCounter += 1
        tk.Button(
            btn_frame, text="Import from Image(s)", command=self.load_palette
        ).grid(row=0, column=columnCounter, padx=5)
        columnCounter += 1
        tk.Button(btn_frame, text="Export GPL", command=self.export_gpl).grid(
            row=0, column=columnCounter, padx=5
        )
        columnCounter += 1
        tk.Button(
            btn_frame, text="Edit Palette", command=self.open_palette_editor
        ).grid(row=0, column=columnCounter, padx=5)
        columnCounter += 1
        tk.Button(btn_frame, text="Clear Palette", command=self.clear_palette).grid(
            row=0, column=columnCounter, padx=5
        )

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_palette(self):
        print("Drawing palette...")
        self.canvas.delete("all")  # clear canvas

        size = 18
        padding = 1
        width = self.canvas.winfo_width()
        cols = max(1, width // (size + padding * 2))
        self.color_label.config(text=f"Colors in palette: {len(self.palette)}")

        for i, (r, g, b) in enumerate(self.palette):
            row = i // cols
            col = i % cols
            x0 = col * (size + padding * 2)
            y0 = row * (size + padding * 2)
            x1 = x0 + size
            y1 = y0 + size
            color_hex = f"#{r:02x}{g:02x}{b:02x}"
            rect = self.canvas.create_rectangle(
                x0, y0, x1, y1, fill=color_hex, outline=""
            )
            # store RGB in a tag
            self.canvas.tag_bind(
                rect,
                "<Enter>",
                lambda e, rgb=(r, g, b): self.color_label.config(text=f"RGB: {rgb}"),
            )
            self.canvas.tag_bind(
                rect,
                "<Leave>",
                lambda e: self.color_label.config(
                    text=f"Colors in palette: {len(self.palette)}"
                ),
            )

        # update scrollregion
        total_rows = (len(self.palette) + cols - 1) // cols
        self.canvas.configure(
            scrollregion=(0, 0, width, total_rows * (size + padding * 2))
        )

    def load_gpl(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("GIMP Palette Files", "*.gpl")]
        )
        if file_path:
            self.palette = read_gpl(file_path)
            self.draw_palette()

    def open_palette_editor(self):
        # Pass main draw function as callback
        PaletteEditorDialog(self.root, self.palette, update_callback=self.draw_palette)

    def load_palette(self):
        def finish_loading(colors, cancelled):
            self.palette = colors
            self.draw_palette()
            if cancelled:
                messagebox.showinfo("Cancelled", "Palette loading was cancelled.")
            else:
                messagebox.showinfo("Done", f"Loaded {len(colors)} unique colors.")

        PaletteLoadDialog(self.root, callback=finish_loading)

    def import_hex_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("#") and len(line) == 7:
                        try:
                            r = int(line[1:3], 16)
                            g = int(line[3:5], 16)
                            b = int(line[5:7], 16)
                            self.palette.append((r, g, b))
                        except ValueError:
                            continue
            self.draw_palette()

    def export_gpl(self):
        if not self.palette:
            messagebox.showwarning("No colors", "Palette is empty!")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".gpl", filetypes=[("GIMP Palette Files", "*.gpl")]
        )
        if file_path:
            with open(file_path, "w") as f:
                f.write("GIMP Palette\n")
                f.write("Name: Exported Palette\n")
                f.write("#\n")
                for r, g, b in self.palette:
                    f.write(f"{r:3d} {g:3d} {b:3d}\n")
            messagebox.showinfo("Exported", f"Palette saved to {file_path}")

    def clear_palette(self):
        self.palette = []
        self.draw_palette()


# Status
@staticmethod
def read_gpl(file_path):
    colors = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if (
                not line
                or line.startswith("#")
                or line.lower().startswith("gimp palette")
                or line.lower().startswith("name:")
            ):
                continue
            parts = line.split()
            if len(parts) >= 3:
                try:
                    r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
                    colors.append((r, g, b))
                except ValueError:
                    continue
    return colors


class PaletteLoadDialog(tk.Toplevel):
    """Combined dialog: choose file/folder, settings, progress, cancel."""

    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Load Palette from File or Folder")
        self.resizable(False, False)
        self.callback = callback
        self.cancelled = False
        self.files = []

        # --- Step 1: Select file or folder ---
        tk.Label(self, text="Select images or folder:").pack(padx=10, pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Select File(s)", command=self.select_files).pack(
            side="left", padx=5
        )
        ttk.Button(btn_frame, text="Select Folder", command=self.select_folder).pack(
            side="right", padx=5
        )

        # --- Step 2: Settings ---
        self.max_colors = tk.IntVar(value=10000)
        self.threshold = tk.DoubleVar(value=0.01)

        settings_frame = ttk.LabelFrame(self, text="Settings")
        settings_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(settings_frame, text="Max Palette Colors:").grid(
            row=0, column=0, sticky="w", padx=5, pady=2
        )
        ttk.Entry(settings_frame, textvariable=self.max_colors, width=10).grid(
            row=0, column=1, padx=5
        )

        ttk.Label(settings_frame, text="Similarity Threshold:").grid(
            row=1, column=0, sticky="w", padx=5, pady=2
        )
        ttk.Entry(settings_frame, textvariable=self.threshold, width=10).grid(
            row=1, column=1, padx=5
        )

        # --- Step 3: Progress bar ---
        self.progress = ttk.Progressbar(self, length=300)
        self.progress.pack(padx=10, pady=10)
        self.progress["value"] = 0

        # --- Step 4: Buttons ---
        btn_frame2 = ttk.Frame(self)
        btn_frame2.pack(pady=5)

        self.start_btn = ttk.Button(
            btn_frame2, text="Start Loading", command=self.start_loading
        )
        self.start_btn.pack(side="left", padx=5)
        ttk.Button(btn_frame2, text="Cancel", command=self.cancel).pack(
            side="right", padx=5
        )

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)

    # --- Select files or folder ---
    def select_files(self):
        paths = filedialog.askopenfilenames(
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if paths:
            self.files = list(paths)
            self.progress["maximum"] = len(self.files)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.files = []
            for root, _, files in os.walk(folder):
                for f in files:
                    if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                        self.files.append(os.path.join(root, f))
            self.progress["maximum"] = len(self.files)

    # --- Cancel ---
    def cancel(self):
        self.cancelled = True
        self.destroy()

    # --- Start loading ---
    def start_loading(self):
        if not self.files:
            messagebox.showwarning("No files", "Please select files or folder first!")
            return

        MAX_COLORS = self.max_colors.get()
        SIMILARITY_THRESHOLD = self.threshold.get()
        unique_colors = []

        def is_too_similar(new_color):
            r1, g1, b1 = new_color
            for r2, g2, b2 in unique_colors:
                dr, dg, db = (r1 - r2) / 255, (g1 - g2) / 255, (b1 - b2) / 255
                if (dr**2 + dg**2 + db**2) ** 0.5 < SIMILARITY_THRESHOLD:
                    return True
            return False

        for idx, img_path in enumerate(self.files):
            print(f"Loading {img_path}")
            if self.cancelled:
                break
            try:
                pixels = Image.open(img_path).convert("RGB").getdata()
                for p in pixels:
                    if self.cancelled:
                        break
                    if not is_too_similar(p):
                        unique_colors.append(p)
                        if len(unique_colors) >= MAX_COLORS:
                            self.cancelled = True
                            break
            except Exception as e:
                print(f"Failed to load {img_path}: {e}")

            # Update progress
            self.progress["value"] = idx + 1
            self.update()  # redraw GUI to show progress and handle Cancel

        self.destroy()
        self.callback(unique_colors, self.cancelled)


import tkinter as tk
from tkinter import ttk, messagebox
import colorsys
import math
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import colorsys
import math


class PaletteEditorDialog(tk.Toplevel):
    def __init__(self, parent, palette, update_callback=None):
        super().__init__(parent)
        self.palette = palette
        self.update_callback = update_callback
        self.title("Palette Editor")
        self.resizable(False, False)

        # --- Merge Frame ---
        merge_frame = ttk.LabelFrame(
            self, text="Merge Similar Colors", padding=(10, 10)
        )
        merge_frame.pack(fill="x", padx=10, pady=10)
        ttk.Label(merge_frame, text="Similarity Threshold (0–1):").grid(
            row=0, column=0, sticky="w"
        )
        self.threshold_var = tk.DoubleVar(value=0.05)
        ttk.Entry(merge_frame, textvariable=self.threshold_var, width=10).grid(
            row=0, column=1, padx=5, sticky="w"
        )
        ttk.Button(
            merge_frame, text="Merge Close Colors", command=self.merge_close_colors
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # --- Append GPL Frame ---
        append_frame = ttk.LabelFrame(self, text="Additional Options", padding=(10, 10))
        append_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(append_frame, text="Append Pallete (GPL File)", command=self.append_gpl).grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        ttk.Button(append_frame, text="Sort Colors", command=self.sort_colors).grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )

        # --- Info Label ---
        self.info_label = ttk.Label(
            self, text=f"Colors in palette: {len(self.palette)}"
        )
        self.info_label.pack(pady=(10, 5))
        # --- Status Label ---
        self.status_label = ttk.Label(self, text="", foreground="blue")
        self.status_label.pack(pady=(5, 10))

        # --- Done Button ---
        done_frame = ttk.Frame(self)
        done_frame.pack(pady=10)
        ttk.Button(done_frame, text="Done", command=self.finish).pack()

        # --- Make modal ---
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.finish)

    # --- Sort palette ---
    def sort_colors(self):
        try:
            colored = []
            grays = []

            for c in self.palette:
                r, g, b = c
                h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
                if s <= 0:
                    grays.append((c, v))
                else:
                    colored.append((c, h, v))

            colored.sort(key=lambda x: (x[1], x[2]))
            grays.sort(key=lambda x: x[1])

            self.palette[:] = [c[0] for c in grays] + [c[0] for c in colored]
            self.status_label.config(text=f"Palette sorted ({len(self.palette)} colors)")
            self.update_main()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort palette: {e}")

    # --- Merge close colors ---
    def merge_close_colors(self):
        try:
            threshold = self.threshold_var.get()
            if threshold <= 0 or threshold > 1:
                messagebox.showwarning(
                    "Invalid Threshold", "Please enter a threshold between 0 and 1."
                )
                return

            merged = []
            for c in self.palette:
                r1, g1, b1 = c
                too_close = False
                for m in merged:
                    r2, g2, b2 = m
                    dr, dg, db = (r1 - r2) / 255, (g1 - g2) / 255, (b1 - b2) / 255
                    if math.sqrt(dr * dr + dg * dg + db * db) < threshold:
                        too_close = True
                        break
                if not too_close:
                    merged.append(c)

            self.palette[:] = merged
            self.status_label.config(
                text=f"Close colors merged ({len(self.palette)} colors)"
            )
            self.update_main()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge colors: {e}")

    # --- Append GPL ---
    def append_gpl(self):
        try:
            files = filedialog.askopenfilenames(filetypes=[("GIMP Palette Files", "*.gpl")])
            if not files:
                return

            added_colors = set(self.palette)
            for f in files:
                new_palette = read_gpl(f)
                for c in new_palette:
                    if c not in added_colors:
                        self.palette.append(c)
                        added_colors.add(c)

            self.status_label.config(
                text=f"Appended {len(added_colors)} colors. Total: {len(self.palette)}"
            )
            self.update_main()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to append colors: {e}")

    # --- Finish dialog ---
    def finish(self):
        self.update_main()
        self.destroy()

    # --- Call main app ---
    def update_main(self):
        if self.update_callback:
            self.update_callback()
        self.info_label.config(text=f"Colors in palette: {len(self.palette)}")


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("725x400")
    app = GPLPaletteManager(root)
    root.mainloop()
