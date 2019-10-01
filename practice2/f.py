from tkinter import *
from tkinter import messagebox
import tkinter
from tkinter import filedialog

def donothing():
   print("a")

def file_save():
	f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
	if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
		return
	text2save = str(text.get(1.0, END)) # starts from `1.0`, not `0.0`
	f.write(text2save)
	f.close() # `()` was missing.

root = Tk()
root.geometry("500x500")
menubar=Menu(root)
text=Text(root)
text.pack()
filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=file_save)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu=Menu(menubar,tearoff=0)
editmenu.add_command(label="Undo", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu=Menu(menubar,tearoff=0)
helpmenu.add_command(label="Help",command=donothing)
menubar.add_cascade(label="Help",menu=helpmenu)

root.config(menu=menubar)
root.mainloop()  