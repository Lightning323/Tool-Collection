import tkinter as tk
from tkinter import filedialog, messagebox
import colorsys
class GPLPaletteManager:
    def __init__(self, root):
        self.root = root
        self.root.title("GPL Palette Manager")

        # Internal palette storage: list of tuples (R,G,B)
        self.palette = []

        # Label for color count
        self.color_label = tk.Label(root, text="Colors in palette: 0")
        self.color_label.pack(pady=5)

        # Scrollable canvas for grid of colors
        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame, bg="white", height=300)
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Inner frame to hold color rectangles
        self.inner_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", self.on_frame_configure)

        # Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Load GPL", command=self.load_gpl).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Append GPL", command=self.combine_gpl).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Import Hex File (.txt)", command=self.import_hex_file).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Export GPL", command=self.export_gpl).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Sort Palette", command=self.sort_palette).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Clear Palette", command=self.clear_palette).grid(row=0, column=5, padx=5)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def draw_palette(self):
        # Update label
        self.color_label.config(text=f"Colors in palette: {len(self.palette)}")

        # Clear previous widgets
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Grid parameters
        cols = 35  # number of columns
        size = 18  # size of each color square
        padding = 0.5

        for i, (r, g, b) in enumerate(self.palette):
            row = i // cols
            col = i % cols
            color_hex = f"#{r:02x}{g:02x}{b:02x}"

            frame = tk.Frame(self.inner_frame, width=size, height=size, bg=color_hex, bd=0, relief="solid")
            frame.grid(row=row, column=col, padx=padding, pady=padding)
            frame.grid_propagate(False)

    def load_gpl(self):
        file_path = filedialog.askopenfilename(filetypes=[("GIMP Palette Files", "*.gpl")])
        if file_path:
            self.palette = self.read_gpl(file_path)
            self.draw_palette()

    def combine_gpl(self):
        files = filedialog.askopenfilenames(filetypes=[("GIMP Palette Files", "*.gpl")])
        if files:
            #Get all colors from the existing palette
            combined = self.palette.copy()
            print(f"Old palette has {len(combined)} colors")
            for f in files:
                new_palette = self.read_gpl(f)
                print(f"New palette has {len(new_palette)} colors")
                combined.extend(new_palette)
                print(f"Combined palette has {len(combined)} colors")
            # Remove duplicates
            seen = set() #Gets all unique colors (Gets e)
            self.palette = []
            for c in combined:
                if c not in seen:
                    self.palette.append(c)
                    seen.add(c)
            print(f"Final palette (unique colors only) has {len(self.palette)} colors")
            self.draw_palette()

    def sort_palette(self):
        def rgb_to_hsv(color):
            r, g, b = color
            # Normalize RGB to 0–1
            return colorsys.rgb_to_hsv(r/255, g/255, b/255)
        colored = []
 

        for c in self.palette:
            h, s, v = rgb_to_hsv(c)
            colored.append((c, h, s, v))  # keep hue & value for sorting

        # Sort colored by hue, then value (dark → light)
        colored.sort(key=lambda x: (x[1], x[3], x[2]))

        # Combine back: colored first, then grays (or flip if you want grays first)
        self.palette = [c[0] for c in colored]

        self.draw_palette()


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
        file_path = filedialog.asksaveasfilename(defaultextension=".gpl", filetypes=[("GIMP Palette Files", "*.gpl")])
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

    @staticmethod
    def read_gpl(file_path):
        colors = []
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or line.lower().startswith("gimp palette") or line.lower().startswith("name:"):
                    continue
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
                        colors.append((r, g, b))
                    except ValueError:
                        continue
        return colors

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("725x400")
    app = GPLPaletteManager(root)
    root.mainloop()
