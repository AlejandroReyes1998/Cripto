from tkinter import * #UI stuff
from tkinter import ttk #UI stuff
from tkinter.filedialog import askopenfilename #UI stuff
from tkinter import messagebox #UI stuff
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import hashlib
import zlib, os

class MyFirstGUI:
	def __init__(self, root):
		self.root = root
		root.geometry('600x300')
		#This code is mine mine mineeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
		self.Title = root.title( "RSA Encrypt/Decrypt App, by Alejandro Reyes")
		self.label = ttk.Label(root, text ="Select your key and file",foreground="red",font=("Segoe UI", 16))
		self.label.pack()
		self.labelsk = ttk.Label(root, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelsk.pack()
		self.keybutton = ttk.Button(root, text="Select Key", command=self.OpenKey)
		self.keybutton.pack()
		self.labelsf = ttk.Label(root, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelsf.pack()
		self.filebutton = ttk.Button(root, text="Select File", command=self.OpenFile)
		self.filebutton.pack()
		self.labelempty = ttk.Label(root, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelempty.pack()
		self.filebuttonhash = ttk.Button(root, text="Hash File", command=self.HashFile)
		self.filebuttonhash.pack()
		self.labelempty2 = ttk.Label(root, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelempty2.pack()
		self.filebuttonhash2 = ttk.Button(root, text="Quick Hash Verify", command=self.VerifyHash)
		self.filebuttonhash2.pack()

		#Menu Bar
		self.menu = Menu(root)
		root.config(menu=self.menu)
		self.file = Menu(self.menu)
		#this closing program method no tho... (same from open file site :p)
		self.file.add_command(label = 'Encrypt file', command = self.EncryptFile)
		self.file.add_command(label = 'Decrypt file', command = self.DecryptFile)
		self.file.add_command(label = 'Exit', command = lambda:exit())
		self.menu.add_cascade(label = 'Options', menu = self.file)
		root.mainloop()


	def OpenFile(self):
		inputfile = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
													 filetypes =(("Text File", "*.txt"),("All Files","*.*")),
													 title = "Choose a file to work with"
													 )
		self.labelsf.config(text=os.path.basename(inputfile))

	def OpenKey(self):
		inputfile = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
													 filetypes =(("PEM File", "*.pem"),("All Files","*.*")),
													 title = "Choose a key to work"
													 )
		self.labelsk.config(text=os.path.basename(inputfile))

	def VerifyHash(self):
		name=self.labelsf.cget("text")
		if not name:
			messagebox.showinfo("Oops!", "Be sure to select a file first!")
		else:
			with open(name,'r') as file_descriptor:	self.file_contents = file_descriptor.read()	
			self.delimiter = '\n__sha2_hash_attribute__\n'
			if self.integrity_check():
				messagebox.showinfo("Success", "The hash is correct!")
			else:
				messagebox.showinfo("Error", "The hash does not correspond to the content of the file.")

	def VerifyHash2(self,output_name):
		with open(output_name,'r') as file_descriptor:	self.file_contents = file_descriptor.read()	
		self.delimiter = '\n__sha2_hash_attribute__\n'
		if self.integrity_checkDEC(output_name):
			return True
		else:
			return False

	def HashFile(self):
		name=self.labelsf.cget("text")
		if not name:
			messagebox.showinfo("Oops!", "Be sure to select a file first!")
		else:
			with open(name,'r') as file_descriptor:	self.file_contents = file_descriptor.read()	
			self.delimiter = '\n__sha2_hash_attribute__\n'
			self.save_hashed("hashed"+name)

	def calculate_hash(self,data):
		message_hash = hashlib.sha256()
		message_hash.update(data.encode('UTF-8')) 
		return message_hash.digest().hex()

		'''
		Esta función guarda el contenido hasheado de la clase.
		Parámetros:
		output_name -- nombre del archivo a guardar.
		'''

	def save_hashed(self,output_name):
		x=self.calculate_hash(self.file_contents)
		with open(output_name,'w')	as file_descriptor:		file_descriptor.write(self.file_contents	+	self.delimiter	+	x)
		with open("signature"+output_name,'w')	as file_descriptor2:		file_descriptor2.write(self.delimiter	+	x)
		messagebox.showinfo("Success", "Message hashed Successfully")
		'''
		Esta función obtiene el contenido o el hash guardados en un archivo de texto.
		Parámetros: 
		content -- 'hash' para obtener el hash guardado. 'message' para obtener el mensaje.
		'''

	def get_original(self,content):
		name=self.labelsf.cget("text")
		self.delimiter = '\n__sha2_hash_attribute__\n'
		with open(name,'r') as file_descriptor:	self.file_contents = file_descriptor.read()	
		try:
			return self.file_contents.split(self.delimiter,1)[0]	if content=='message' else	self.file_contents.split(self.delimiter,1)[1]			
		except IndexError:	
			messagebox.showinfo("Error", "This file hasn't been hashed yet!")

	def get_originalDEC(self,content,output_name):	
		self.delimiter = '\n__sha2_hash_attribute__\n'
		with open(output_name,'r') as file_descriptor:	self.file_contents = file_descriptor.read()	
		try:
			return self.file_contents.split(self.delimiter,1)[0]	if content=='message' else	self.file_contents.split(self.delimiter,1)[1]			
		except IndexError:	
			messagebox.showinfo("Error", "This file hasn't been hashed yet!")
			


	def integrity_check(self):	return True if self.get_original('hash') == self.calculate_hash(self.get_original('message')) else False

	def integrity_checkDEC(self,output_name):	return True if self.get_originalDEC('hash',output_name) == self.calculate_hash(self.get_originalDEC('message',output_name)) else False


	def EncryptFile(self):
		file=self.labelsf.cget("text")
		with open(file,'rb') as file_descriptor:	self.file_contents = file_descriptor.read()	
		outputName="EncryptedRSA_"+file
		publicKey=self.labelsk.cget("text")
		if not outputName:
			messagebox.showinfo("Oops!", "Be sure to select a file first!")
		else:
			if not publicKey:
				messagebox.showinfo("Oops!", "Be sure to select a public Key first!")
			else:
				with open(publicKey, "rb") as pub_key:
					blob = self.encrypt_blob(self.file_contents, pub_key.read())
					with open(outputName, "wb") as encrypted_file:
						encrypted_file.write(blob)
				messagebox.showinfo("Success", "Message Encrypted Successfully")

		'''
		Descifrar un archivo usando RSA.

		Parámetros:
		outputName  -- Nombre para con el cual se debería guardar el archivo.
		privateKey   -- Archivo que contiene la llave privada.
		'''

	def DecryptFile(self):
		file=self.labelsf.cget("text")
		with open(file,'rb') as file_descriptor:	self.file_contents = file_descriptor.read()	
		outputName="DecryptedRSA_"+file
		privateKey=self.labelsk.cget("text")
		if not outputName:
			messagebox.showinfo("Oops!", "Be sure to select a file first!")
		else:
			if not privateKey:
				messagebox.showinfo("Oops!", "Be sure to select a Key first!")
			else:
				with open(privateKey, "rb") as priv_key:
					try:
						decrypted_blob = self.decrypt_blob(self.file_contents, priv_key.read())
						with open(outputName, "wb") as decrypted_file:
							decrypted_file.write(decrypted_blob)
						if self.VerifyHash2(outputName):
							messagebox.showinfo("Success", "Message Decrypted Successfully. The hash is valid")
						else:
							messagebox.showinfo("Error", "The hash does not correspond to the content of the file. Please verify that the message hasn't been modified")
					except Exception as e:
						messagebox.showinfo("Error", "Something wrong happened during the decryption process, make sure that you are using the correct key or that the message hasn't been modifed.")
						print(e)



	def encrypt_blob(self, blob, public_key):
		'''
		Para determinar qué tan grande puede ser un chunk, se usa la longitud de la llave privada en bytes 
		y se le restan 42 bytes (PKCS1_OAEP). Cada chunk después se cifra individualmente.
		'''
		rsaKey = RSA.importKey(public_key)
		chunk_size = rsaKey.size_in_bytes() - 42
		rsaKey = PKCS1_OAEP.new(rsaKey)
		blob = zlib.compress(blob)    
		offset = 0
		endOfFile = False
		encrypted = bytes()
		blob_len  = len(blob)//chunk_size if(len(blob)>=chunk_size) else len(blob)
		encryptedCount = 0

		while not endOfFile:
			chunk = blob[offset:offset + chunk_size]

			'''
			Se llegó al final del archivo, pero este puede necesitar padding. Agregar bytes de sobra para 
			poder cifrar este chunk.
			'''

			if len(chunk) % chunk_size != 0:
				endOfFile = True
				length  =   (chunk_size - len(chunk)) % chunk_size
				chunk += bytes([length])*length

			print("Encrypted so far (%): ",(encryptedCount/blob_len)*100,end='\r')
			encrypted += rsaKey.encrypt(chunk)
			encryptedCount += 1
			offset += chunk_size
		return encrypted

	def decrypt_blob(self,blob, private_key):  
		rsakey = RSA.importKey(private_key)
		chunk_size = rsakey.size_in_bytes()
		rsakey = PKCS1_OAEP.new(rsakey)
		offset = 0
		decrypted = bytes()
		blob_len  = len(blob)//chunk_size if(len(blob)>=chunk_size) else len(blob)
		decryptedCount = 0

		while offset < len(blob):
			chunk = blob[offset: offset + chunk_size]
			decrypted += rsakey.decrypt(chunk)
			offset += chunk_size
			decryptedCount += 1
			print("Decrypted so far (%): ",(decryptedCount/blob_len)*100,end='\r')

		return zlib.decompress(decrypted)


root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()