from tkinter import * #UI stuff
from tkinter import ttk #UI stuff
from tkinter.filedialog import askopenfilename #UI stuff
from tkinter import messagebox #UI stuff
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import zlib, os
class MyFirstGUI:
	def __init__(self, root):
		self.root = root
		root.geometry('300x120')
		#This code is mine mine mineeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
		self.Title = root.title( "RSA Key Generator, by Alejandro Reyes")
		self.labelkg = ttk.Label(root, text ="Key Generator",foreground="blue",font=("Segoe UI", 16))
		self.labelkg.pack()
		self.label2 = ttk.Label(root, text ="Insert a name for your key",foreground="blue",font=("Segoe UI", 12))
		self.label2.pack()
		self.txtk = Entry(root,width=20)
		self.txtk.pack()
		self.kgbutton = ttk.Button(root, text="Generate Keys", command=self.keygenerator)
		self.kgbutton.pack()

		#Menu Bar
		self.menu = Menu(root)
		root.config(menu=self.menu)
		self.file = Menu(self.menu)
		#this closing program method no tho... (same from open file site :p)
		self.file.add_command(label = 'Exit', command = lambda:exit())
		self.menu.add_cascade(label = 'Options', menu = self.file)
		root.mainloop()

	def keygenerator(self):
		privateKeyName=self.txtk.get()+'_private.pem'
		publicKeyName=self.txtk.get()+'_public.pem'
		new_key = RSA.generate(2048, e=65537)
		private_key = new_key.exportKey('PEM')
		public_key = new_key.publickey().exportKey('PEM')

		with open(privateKeyName,'wb') as privateKeyFile,   open(publicKeyName,'wb') as publicKeyFile:
			privateKeyFile.write(private_key)
			publicKeyFile.write(public_key)
		messagebox.showinfo("Success","Pair of keys generated succesfully!, Be sure to share them correctly")
		

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()