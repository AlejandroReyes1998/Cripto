from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from tkinter import filedialog


root = Tk(  )

#This is where we lauch the file manager bar.
def EncryptFile():
		name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
													 filetypes =(("Text File", "*.txt"),("All Files","*.*")),
													 title = "Choose a file to Encrypt"
													 )
		inputx = txt.get()
		flag=True
		try:
			int_x=int(inputx)
			if(int_x <= 255 and int_x >= 1):
				print("cool")
			else:
				print("Try again")
				flag=False
		except:
				print("not a number m8")
				flag=False

		if(flag):
			#Using try in case user types in unknown file or closes without choosing a file.
			try:
					filex=open(name, 'r')
					contenido=filex.read()
					filex.close()
					palabras=[]
					for line in contenido:     
						for char in line:    
								try:
									palabras.append(chr((ord(char)+int_x)%255)) #ord nos devuelve el valor de ascii para sumarlo con el de la llave y obtener el nuevo valor  
								except Exception as e:
									print(e)
									palabras.append("[E: "+char+"]")
					x=''.join(palabras)
					print("file Encrypted")
					try:
						filex=open('c.txt', 'w', encoding="utf-8")
						filex.write(x)
						filex.close()
						messagebox.showinfo("Success", "The file has been encrypted successfully")
					except Exception as e:
						print(e)					
			except Exception as e:
					print(e)
					messagebox.showinfo("Error", "An error has ocurred, try again: "+e)
		else:
			messagebox.showinfo("Error", "The key is invalid, try again")

#This is where we lauch the file manager bar.
def DecryptFile():
		name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
													 filetypes =(("Text File", "*.txt"),("All Files","*.*")),
													 title = "Choose a file to Decrypt"
													 )
		inputx = txt.get()
		flag=True
		try:
			int_x=int(inputx)
			if(int_x <= 255 and int_x >= 1):
				print("cool")
			else:
				print("Try again")
				flag=False
		except:
				print("not a number m8")
				flag=False

		if(flag):
			#Using try in case user types in unknown file or closes without choosing a file.
			try:
					filex=open(name, 'r', encoding="utf-8")
					contenido=filex.read()
					filex.close()
					palabras=[]
					for line in contenido:     
						for char in line:    
								try:
									if((ord(char)+(-int_x))<0):
										palabras.append(chr((ord(char)+(-int_x))%255)) #ord nos devuelve el valor de ascii para sumarlo con el de la llave y obtener el nuevo valor  
									else:
										xw=chr(ord(char)+(-int_x))
										palabras.append(xw)
								except Exception as e:
									print(e)
									palabras.append("[E: "+char+"]")
					x=''.join(palabras)
					print("file Decrypted")
					try:
						filex=open('m.txt', 'w', encoding="utf-8")
						filex.write(x)
						filex.close()
						messagebox.showinfo("Success", "The file has been decrypted successfully")
					except Exception as e:
						print(e)					
			except Exception as e:
					print(e)
					messagebox.showinfo("Error", "An error has ocurred, try again: "+e)
		else:
			messagebox.showinfo("Error", "The key is invalid, try again")


root.geometry('600x100')
Title = root.title( "Shift Cipher, by Alejandro Reyes")
label = ttk.Label(root, text ="Enter a key (1 to 255)",foreground="blue",font=("Helvetica", 16))
label.pack()
txt = Entry(root,width=20)
txt.pack()

#Menu Bar
menu = Menu(root)
root.config(menu=menu)
file = Menu(menu)
file.add_command(label = 'Encrypt file', command = EncryptFile)
file.add_command(label = 'Decrypt file', command = DecryptFile)
file.add_command(label = 'Exit', command = lambda:exit())
menu.add_cascade(label = 'File', menu = file)
root.mainloop()