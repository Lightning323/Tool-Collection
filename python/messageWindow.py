import tkinter as tk
import tkinter.ttk as ttk


def set_width(window, width):
    window.geometry("{}x{}".format(width, window.winfo_height()))


class PopupWindow():
    def __init__(self, path, title, body):
        self.root = tk.Tk()
        ttk.Style().theme_use('xpnative')
        self.root.title(title)
        self.root.config(padx=25, pady=10)
        self.root.iconbitmap(path + "/resources/icon.ico")

        # make this one bolded
        self.lt = ttk.Label(self.root, text=title,
                            font=("Helvetica", 9, 'bold'))
        self.lt.pack()

        self.l = ttk.Label(self.root, text=body)
        self.l.pack()
        self.b = ttk.Button(self.root, text="OK", command=self.cleanup)
        self.b.pack(padx=5, pady=10)
        self.root.resizable(0, 0)
        # if self.root.winfo_width() < 300:
        #     set_width(self.root, 300)
        # elif self.root.winfo_width() > 600:
        #     set_width(self.root, 600)
        self.root.mainloop()

    def cleanup(self):
        self.root.destroy()



