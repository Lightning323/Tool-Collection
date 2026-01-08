# create a new tkinter window
from tkinter import *
from tkinter import ttk
import tkinter as tk
import os
from tkinter import filedialog
import calculatorAPI as calc

class GcodeEditor:
    def __init__(self):
        root = calc.createRootWindow("GCODE Editor")
        label = calc.header(root, text="GCODE Editor")
        label.config(width=30)
        label.pack(pady=10)

        grid = Frame(root)
        grid.pack()

        #Make some text explaining what the below button does
        label = tk.Label(root, text="Select GCODE file to heat up buildplate and hotend at the same time")
        # enable the label to wrap the text
        label.bind('<Configure>', lambda e: label.config(wraplength=label.winfo_width()))
        label.config(width=30)
        label.pack(pady=20)

        button = tk.Button(root, text='Open GCODE and Convert', command=uploadFile)
        button.pack(pady=5)

        button = tk.Button(root, text='Convert All GCODEs in Directory', command=uploadDirectory)
        button.pack(pady=5)

        root.eval('tk::PlaceWindow . center') #Center the root window
        root.mainloop()


def uploadFile(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    
    #Only convert gcode files if they end in .gcode
    if filename.endswith(".gcode"):
        convertGCODE(filename)
        calc.PopupWindow("Not implemented", "GCODE file has not been converted.")
    else:
        calc.PopupWindow("Error", "Please select a GCODE file.")

def uploadDirectory(event=None):
    filename = filedialog.askdirectory()
    print('Selected:', filename)
    convertAllGCODES(filename)
   


def convertAllGCODES(dir):
    i = 0
    for filename in os.listdir(dir):
        if filename.endswith(".gcode"):
            convertGCODE(dir+"/"+filename)
            i += 1
    calc.PopupWindow("Not implemented", f"{i} GCODE files have not been converted.")

def convertGCODE(filename):
    print("NOT Converting: " + filename)
    #with open(filename, "r") as file:
    #    lines = file.readlines()
    #for i in range(len(lines)):
	# TODO: This not only prevents cooldown but also changes bed temprature. Make this more reliable.
        #if "M140 S" in lines[i]: #Set bed temprature
        #    lines[i] = "M140 S50\n"
        #elif "M104 S" in lines[i]: #Set hotend temprature
        #    lines[i] = "M190 S50\n"
        #elif "M190 S" in lines[i]: #wait for bed temprature
        #    lines[i] = "M104 S185\n"
        #elif "M109 S" in lines[i]: #wait for hotend temprature
        #    lines[i] = "M109 S185\n"
    #lines = [line for line in lines if "M105" not in line] # remove first two M105 lines
    #with open(filename, "w") as file:
    #    file.writelines(lines)

# GcodeEditor()
