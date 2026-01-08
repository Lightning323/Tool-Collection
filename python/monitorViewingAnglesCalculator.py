import math
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image, ImageTk, ImageDraw

class EdgeColorApp:
    def __init__(self, master=None, width=400, height=300):
        self.width = width
        self.height = height

        # Use provided master or create a new root
        self.root = tk.Toplevel(master) if master else tk.Tk()
        self.root.title("Viewing Angle Edge Color Simulation")
        self.root.geometry(f"{width+60}x{height+60}")
        self.root.resizable(False, False)

        # Canvas for displaying the image
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        # Entry for value 0-1
        tk.Label(self.root, text="Edge shift (0 (black) - 1 (white)):").grid(row=1, column=0, sticky="w", padx=10)
        self.var = tk.StringVar(value="1")
        self.entry = tk.Entry(self.root, textvariable=self.var, width=10)
        self.entry.grid(row=1, column=0, sticky="e", padx=10)

        # Bind entry changes to update function
        self.var.trace_add("write", lambda *args: self.update_image_color())

        # Keep reference to PhotoImage
        self.tk_img = None

        # Initial image
        self.update_image_color()

    def generate_image(self, factor):
        factor = max(0.0, min(1.0, factor))
        width, height = self.width, self.height
        cx, cy = width / 2, height / 2

        center_color = (255, 255, 255)      # Fixed center
        edge_color = (int(255 * factor), int(255 * factor), int(255 * factor))  # Edge changes

        img = Image.new("RGB", (width, height), color=center_color)
        draw = ImageDraw.Draw(img)

        max_dist = (cx ** 2 + cy ** 2) ** 0.5

        for y in range(height):
            for x in range(width):
                dx = x - cx
                dy = y - cy
                dist = (dx ** 2 + dy ** 2) ** 0.5
                local_factor = dist / max_dist
                r = int(center_color[0] + local_factor * (edge_color[0] - center_color[0]))
                g = int(center_color[1] + local_factor * (edge_color[1] - center_color[1]))
                b = int(center_color[2] + local_factor * (edge_color[2] - center_color[2]))
                draw.point((x, y), fill=(r, g, b))

        return img

    def update_image_color(self):
        try:
            factor = float(self.var.get())
        except ValueError:
            factor = 0.5
        factor = max(0.0, min(1.0, factor))

        img = self.generate_image(factor)
        self.tk_img = ImageTk.PhotoImage(img)  # Keep reference
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        # Draw border
        border_size = 4
        self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            outline="black", width=border_size
        )


























































def calculate_dimensions(diagonal, aspect_ratio_width, aspect_ratio_height):
    ratio_diagonal = math.sqrt(aspect_ratio_width**2 + aspect_ratio_height**2)
    width = diagonal * (aspect_ratio_width / ratio_diagonal)
    height = diagonal * (aspect_ratio_height / ratio_diagonal)
    return width, height


def compute_view_angles(width, height, distance):
    half_w = width / 2
    half_h = height / 2
    half_horizontal = math.degrees(math.atan(half_w / distance))
    half_vertical = math.degrees(math.atan(half_h / distance))
    half_diagonal = math.degrees(math.atan(math.hypot(half_w, half_h) / distance))
    return {
        "half_horizontal_deg": half_horizontal,
        "full_horizontal_deg": half_horizontal * 2,
        "half_vertical_deg": half_vertical,
        "full_vertical_deg": half_vertical * 2,
        "half_diagonal_deg": half_diagonal,
        "full_diagonal_deg": half_diagonal * 2,
    }


def plot_screen_view(ax, width, height, distance, angles):
    ax.clear()
    w2, h2 = width / 2, height / 2

    corners = {
        "top-right": (w2, h2, distance),
        "top-left": (-w2, h2, distance),
        "bottom-left": (-w2, -h2, distance),
        "bottom-right": (w2, -h2, distance),
    }

    # Screen rectangle
    verts = [[corners["top-right"], corners["top-left"], corners["bottom-left"], corners["bottom-right"]]]
    ax.add_collection3d(Poly3DCollection(verts, alpha=0.2, facecolor="blue"))

    # Rays to corners
    for x, y, z in corners.values():
        ax.plot([0, x], [0, y], [0, z], "k--")
        ax.scatter([x], [y], [z], s=20)

    # Angle reference points
    ax.scatter([w2], [0], [distance], color="green", s=60, label=f"Half H {angles['half_horizontal_deg']:.1f}°")
    ax.scatter([w2], [h2], [distance], color="lime", s=60, label=f"Full H {angles['full_horizontal_deg']:.1f}°")
    ax.scatter([0], [h2], [distance], color="blue", s=60, label=f"Half V {angles['half_vertical_deg']:.1f}°")
    ax.scatter([w2], [h2], [distance], color="cyan", s=60, label=f"Full V {angles['full_vertical_deg']:.1f}°")
    ax.scatter([w2 / 2], [h2 / 2], [distance], color="orange", s=60, label=f"Half D {angles['half_diagonal_deg']:.1f}°")
    ax.scatter([w2], [h2], [distance], color="magenta", s=60, label=f"Full D {angles['full_diagonal_deg']:.1f}°")

    # Axes settings
    max_range = max(width, height, distance) * 0.6
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(0, max_range*2)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=0, azim=90)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1), fontsize=8)
    ax.set_title("3D Viewing Geometry")


class ScreenCalculatorApp:
    def __init__(self):
        # Main window
        self.root = tk.Tk()
        self.root.title("Screen Viewing Angle Calculator")
        self.root.geometry("810x400")
        self.root.resizable(False, False)

        # Main frame
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Tkinter variables bound to root
        self.diag_var = tk.StringVar(master=self.root, value="27")
        self.aspect_w_var = tk.StringVar(master=self.root, value="16")
        self.aspect_h_var = tk.StringVar(master=self.root, value="9")
        self.distance_var = tk.StringVar(master=self.root, value="24")

        # Input fields
        self.create_input("Screen Diagonal (inches):", self.diag_var, 0)
        self.create_input("Aspect Ratio Width:", self.aspect_w_var, 1)
        self.create_input("Aspect Ratio Height:", self.aspect_h_var, 2)
        self.create_input("Viewing Distance (inches):", self.distance_var, 3)

        # Update button
        ttk.Button(self.frame, text=" Update ", command=self.update_plot).grid(row=4, column=0, columnspan=2, pady=5)

        ttk.Button(self.frame, text=" + Color Tester ", command=lambda: EdgeColorApp(master=self.root, width=450, height=int(450 * float(self.aspect_h_var.get()) / float(self.aspect_w_var.get())))).grid(row=5, column=0, columnspan=2, pady=5)

        # Output labels
        self.width_label = ttk.Label(self.frame, text="Width: ")
        self.width_label.grid(row=6, column=0, columnspan=2)
        self.height_label = ttk.Label(self.frame, text="Height: ")
        self.height_label.grid(row=7, column=0, columnspan=2)
        self.distance_label = ttk.Label(self.frame, text="Distance: ")
        self.distance_label.grid(row=8, column=0, columnspan=2)
        self.angles_label = ttk.Label(self.frame, text="Angles: ", justify="left")
        self.angles_label.grid(row=9, column=0, columnspan=2)

        # Matplotlib figure
        self.fig = plt.Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10)

        # Set defaults explicitly (ensures they show when imported)
        self.diag_var.set("27")
        self.aspect_w_var.set("16")
        self.aspect_h_var.set("9")
        self.distance_var.set("24")

        # Initial plot
        self.update_plot()

    def create_input(self, label_text, variable, row):
        ttk.Label(self.frame, text=label_text).grid(row=row, column=0, sticky="e")
        ttk.Entry(self.frame, textvariable=variable, width=10).grid(row=row, column=1)

    def update_plot(self):
        try:
            diag = float(self.diag_var.get())
            ar_w = float(self.aspect_w_var.get())
            ar_h = float(self.aspect_h_var.get())
            dist = float(self.distance_var.get())
        except ValueError:
            return

        width, height = calculate_dimensions(diag, ar_w, ar_h)
        angles = compute_view_angles(width, height, dist)

        self.width_label.config(text=f"Width: {width:.2f} in")
        self.height_label.config(text=f"Height: {height:.2f} in")
        self.distance_label.config(text=f"Distance: {dist:.2f} in")
        self.angles_label.config(
            text="\n".join([f"{k}: {v:.2f}°" for k, v in angles.items()])
        )

        plot_screen_view(self.ax, width, height, dist, angles)
        self.canvas.draw()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ScreenCalculatorApp()
    app.run()
