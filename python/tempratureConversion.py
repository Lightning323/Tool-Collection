# create a new tkinter window
from tkinter import *
from tkinter import ttk
import calculatorAPI as calc

class CelciusFarenheit:
    def __init__(self):
        root = calc.createRootWindow("Calculator")
        label = calc.header(root, text="Farenheit / Celcius Calculator")
        label.config(width=33)
        label.pack(pady=5)

        grid = Frame(root)
        grid.pack()

        self.f = calc.InputBox(grid, "Temp Farenheit",0,width = 24, onchangeEvent=self.calculateC)
        self.c = calc.InputBox(grid, "Temp Celcius",1,width = 24, onchangeEvent=self.calculateF)

        # button = ttk.Button(root, text="Calculate", command=self.calculate)
        # button.pack(pady=5, fill=X)
        button = ttk.Button(root, text="Clear", command=self.clear)
        button.pack(pady=5, fill=X)
        root.mainloop()

    def calculateF(self,event):
        c = self.c.getValue()
        f = c * 9 / 5 + 32
        self.f.setValue(round(f,2))

    def calculateC(self,event):
        f = self.f.getValue()
        c = (f - 32) * 5 / 9
        self.c.setValue(round(c,2))

    def clear(self):
        self.f.setValue("")
        self.c.setValue("")