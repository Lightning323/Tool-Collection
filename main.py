# create a new tkinter window
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk
import calculatorAPI as calc
import tkinter.ttk as ttk
import filamentCalculator as fc
import tempratureConversion as temp
import gcodeEditor as gcode2
import monitorViewingAnglesCalculator as mvac

root = calc.createRootWindow("Multi Tool")
label = calc.header(root, text="Multi Tool Main Menu")

import webbrowser
import os



def filament():
    fc.FilamentCalculator()

def tempC():
    temp.CelciusFarenheit()

def palleteEditor():
    gcode2.PalleteEditor()

def htmlTools():
    filename = 'file:///'+os.getcwd()+'/' + 'html/index.html'
    webbrowser.open_new_tab(filename)

def pickColor():
    color = askcolor(title="Color Chooser Dialog")
    #copy the color to the clipboard
    root.clipboard_append(color)
    print(color)

def gcode():
    gcode2.GcodeEditor()

def viewingAngles():
    app = mvac.ScreenCalculatorApp()
    app.run()

def menuButton(text, command2):
    button = ttk.Button(root, text=text, command=command2,width=50)
    button.pack(pady=5, fill=X, ipady=5)
    return button


menuButton("Filament Calculator", filament)
menuButton("Color Picker", pickColor)
menuButton("Temprature Conversion", tempC)
menuButton("GCODE Editor", gcode)
menuButton("HTML Tools", htmlTools)
menuButton("Monitor Viewing Angles", viewingAngles)
menuButton("Pallete Editor", palleteEditor)


filler = ttk.Label(root, text="")
filler.pack(pady=40, fill=X)

root.mainloop()

