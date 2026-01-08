import tkinter as tk
from tkinter import filedialog, messagebox
import colorsys
from PIL import Image
import os

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
        tk.Button(btn_frame, text="Load Folder to Palette", command=self.load_images_to_palette).grid(row=0, column=6, padx=5)

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

            # Bind hover events
            def on_enter(event, r=r, g=g, b=b):
                self.color_label.config(text=f"RGB: ({r}, {g}, {b})")

            def on_leave(event):
                self.color_label.config(text=f"Colors in palette: {len(self.palette)}")

            frame.bind("<Enter>", on_enter)
            frame.bind("<Leave>", on_leave)


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
        grays = []

        for c in self.palette:
            h, s, v = rgb_to_hsv(c)
            if s <= 0:
                grays.append((c, v))  # keep value for sorting dark→light
            else:
                colored.append((c, h, v))  # keep hue & value for sorting

        # Sort colored by hue, then value (dark → light)
        colored.sort(key=lambda x: (x[1], x[2]))

        # Sort grays by value (dark → light)
        grays.sort(key=lambda x: x[1])

        # Combine back: colored first, then grays (or flip if you want grays first)
        # Combine back: grays first, then colored hues
        self.palette = [c[0] for c in grays] + [c[0] for c in colored]
        self.draw_palette()


    def load_images_to_palette(self):
        # Ask user to select either a single file or a folder
        choice = messagebox.askquestion("Load Images", "Do you want to load a single image file?\n\nYes = file, No = folder")
        
        file_count = 0
        all_colors = []
        max_colors = 256  # optional limit

        if choice == "yes":
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
            if not file_path:
                return
            try:
                img = Image.open(file_path).convert("RGB")
                pixels = list(img.getdata())
                all_colors.extend(pixels)
                print(f"Loaded {len(pixels)} pixels from {file_path}")
            except Exception as e:
                print(f"Failed to load {file_path}: {e}")
        else:
            folder_path = filedialog.askdirectory()
            if not folder_path:
                return
            print(f"\n\nSearching folder recursively: {folder_path}")
            for root_dir, dirs, files in os.walk(folder_path):
                print(f"Searching {root_dir}")
                for filename in files:
                    file_count += 1
                    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                        img_path = os.path.join(root_dir, filename)
                        try:
                            img = Image.open(img_path).convert("RGB")
                            pixels = list(img.getdata())
                            all_colors.extend(pixels)
                            print(f"Loaded {len(pixels)} pixels from {img_path}")
                        except Exception as e:
                            print(f"Failed to load {img_path}: {e}")

        # Remove duplicates
        unique_colors = list(dict.fromkeys(all_colors))

        # Limit to max_colors
        self.palette = unique_colors[:max_colors] if max_colors else unique_colors

        self.draw_palette()
        messagebox.showinfo("Palette Loaded", f"{len(self.palette)} unique colors loaded from {file_count} files.")

    
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
