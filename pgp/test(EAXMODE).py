#!/usr/bin/env python
# -*- coding: utf-8 -*-
#https://pycryptodome.readthedocs.io/en/latest/src/examples.html
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename #UI stuff
from tkinter import messagebox #UI stuff
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes as r
from Crypto.Cipher import AES, PKCS1_OAEP
import zlib, os

class ConfidentialityFrame(ttk.Frame):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.style = ttk.Style()
		self.label = ttk.Label(self, text ="This mode only requires to Encrypt/Decrypt with your key, no Signature needed",foreground="blue",font=("Segoe UI", 11))
		self.label.pack()

		self.labelsk = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelsk.pack()
		self.keybutton = ttk.Button(self, text="Select Key", command=self.OpenKey)
		self.keybutton.pack()
		
		self.labelsf = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelsf.pack()
		self.filebutton = ttk.Button(self, text="Select File", command=self.OpenFile)
		self.filebutton.pack()

		self.labele1 = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labele1.pack()
		self.Encryptbutton = ttk.Button(self, text="Encrypt File", command=self.EncryptFile)
		self.Encryptbutton.pack()

		self.labele2 = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labele2.pack()
		self.Decryptbutton = ttk.Button(self, text="Decrypt File", command=self.DecryptFile)
		self.Decryptbutton.pack()
	
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

	def EncryptFile(self):
		file=self.labelsf.cget("text")
		with open(file,'rb') as file_descriptor:	self.file_contents = file_descriptor.read()	
		outputName="(C-MODE)Encrypted_RSA_AES_"+file
		publicKey=self.labelsk.cget("text")
		if not outputName:
			messagebox.showinfo("Oops!", "Make sure to select a file first!")
		else:
			if not publicKey:
				messagebox.showinfo("Oops!", "Make sure to select a public Key first!")
			else:
				try:
					file_out = open(outputName, "wb")

					recipient_key = RSA.import_key(open(publicKey).read())
					session_key = r.get_random_bytes(16)

					# Encrypt the session key with the public RSA key
					cipher_rsa = PKCS1_OAEP.new(recipient_key)
					enc_session_key = cipher_rsa.encrypt(session_key)

					# Encrypt the data with the AES session key
					cipher_aes = AES.new(session_key, AES.MODE_EAX)
					ciphertext, tag = cipher_aes.encrypt_and_digest(self.file_contents)
					[ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
					messagebox.showinfo("Success", "Message Encrypted Successfully")
				except Exception as e:
					messagebox.showinfo("Error", "Something wrong happened...")
					print(e)

	def DecryptFile(self):
		file=self.labelsf.cget("text")
		with open(file,'rb') as file_descriptor:	self.file_contents = file_descriptor.read()	
		outputName="(C-MODE)Decrypted_RSA_AES_"+file
		privateKey=self.labelsk.cget("text")
		if not outputName:
			messagebox.showinfo("Oops!", "Make sure to select a file first!")
		else:
			if not privateKey:
				messagebox.showinfo("Oops!", "Make sure to select a Key first!")
			else:
				with open(privateKey, "rb") as priv_key:
					try:
						private_key = RSA.import_key(priv_key.read())
						with open(file,'rb') as file_descriptor:
							enc_session_key, nonce, tag, ciphertext = \
							   [ file_descriptor.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

						# Decrypt the session key with the private RSA key
						cipher_rsa = PKCS1_OAEP.new(private_key)
						session_key = cipher_rsa.decrypt(enc_session_key)

						# Decrypt the data with the AES session key
						cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
						data = cipher_aes.decrypt_and_verify(ciphertext, tag)
						with open(outputName, "wb") as decrypted_file:
							decrypted_file.write(data)
							messagebox.showinfo("Success", "Message Decrypted Successfully.")
					except Exception as e:
						messagebox.showinfo("Error", "The key is invalid")
						print(e)

class AuthenticityFrame(ttk.Frame):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.style = ttk.Style()
		self.label = ttk.Label(self, text ="This mode only verifies the sender with your key, no encryption needed",foreground="red",font=("Segoe UI", 11))
		self.label.pack()

		self.labelsk = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelsk.pack()
		self.keybutton = ttk.Button(self, text="Select Key", command=self.OpenKey)
		self.keybutton.pack()
		
		self.labelsf = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelsf.pack()
		self.filebutton = ttk.Button(self, text="Select File", command=self.OpenFile)
		self.filebutton.pack()

		self.labelemptySI = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelemptySI.pack()
		self.filebuttonhash = ttk.Button(self, text="Hash File", command=self.HashFile)
		self.filebuttonhash.pack()

		self.labelempty2 = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelempty2.pack()
		self.filebuttonhash2 = ttk.Button(self, text="Hash Verify", command=self.VerifyHash)
		self.filebuttonhash2.pack()
	
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
		thekey=self.labelsk.cget("text")
		delimiter = '\n__sha2_hash_attribute__\n'
		if not name:
			messagebox.showinfo("Oops!", "Be sure to select a file first!")
		else:			
			if not thekey:
				messagebox.showinfo("Oops!", "Be sure to select a public key!")
			else:
				with open(name,'rb') as file_descriptor:	self.file_contents = file_descriptor.read()
				try:
					hash_archivo=self.file_contents.split(delimiter.encode(),1)[1]
					contenido=self.file_contents.split(delimiter.encode(),1)[0]
					# print("------------HASH-----------")
					# print(hash_archivo)
					# print("------------contenido-----------")
					# print(contenido)
					key = RSA.import_key(open(thekey).read())
					h = SHA256.new(contenido)
					try:
						pkcs1_15.new(key).verify(h,hash_archivo)
						messagebox.showinfo("Success", "The hash is authentic")
					except (ValueError, TypeError) as e:
						print(e)
						messagebox.showinfo("Warning!", "The hash is incorrect")
				except IndexError:
					messagebox.showinfo("Warning!", "Your text file doesn't contain a hash")
				
				

	def HashFile(self):
		name=self.labelsf.cget("text")
		thekey=self.labelsk.cget("text")
		if not name:
			messagebox.showinfo("Oops!", "Make sure to select a file first!")
		else:
			if not thekey:
				messagebox.showinfo("Oops!", "Make sure to select a private key first!")
			else:
				with open(name,'r') as file_descriptor:	self.file_contents = file_descriptor.read()	
				key = RSA.import_key(open(thekey).read())
				h = SHA256.new(self.file_contents.encode('utf8'))
				signature = pkcs1_15.new(key).sign(h)
				delimiter = '\n__sha2_hash_attribute__\n'
				with open(name,'wb')	as file_descriptor:		file_descriptor.write(self.file_contents.encode()	+	delimiter.encode()	+	signature)
				messagebox.showinfo("Success", "File Hashed")

class FullFrame(ttk.Frame):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.style = ttk.Style()
		self.label = ttk.Label(self, text ="This mode offers both Authenticity and Confidentiality",foreground="purple",font=("Segoe UI", 11))
		self.label.pack()

		self.labelpublick = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelpublick.pack()
		self.keybuttonpubk = ttk.Button(self, text="Select Public Key", command=self.OpenPublicKey)
		self.keybuttonpubk.pack()
		
		self.labelprivatek = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelprivatek.pack()
		self.keybuttonprivk = ttk.Button(self, text="Select Private Key", command=self.OpenPrivateKey)
		self.keybuttonprivk.pack()

		self.labelsf = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelsf.pack()
		self.filebutton = ttk.Button(self, text="Select File", command=self.OpenFile)
		self.filebutton.pack()

		self.labelemptySI = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelemptySI.pack()
		self.filebuttonhash = ttk.Button(self, text="Encrypt & Hash", command=self.EncryptnHash)
		self.filebuttonhash.pack()

		self.labelempty2 = ttk.Label(self, text ="",foreground="black",font=("Segoe UI", 10))
		self.labelempty2.pack()
		self.filebuttonhash2 = ttk.Button(self, text="Decrypt & Verify", command=self.DecryptnVerify)
		self.filebuttonhash2.pack()

	def OpenFile(self):
		inputfile = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
													 filetypes =(("Text File", "*.txt"),("All Files","*.*")),
													 title = "Choose a file to work with"
													 )
		self.labelsf.config(text=os.path.basename(inputfile))

	def OpenPublicKey(self):
		inputfile = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
													 filetypes =(("PEM File", "*.pem"),("All Files","*.*")),
													 title = "Choose a public key to work"
													 )
		self.labelpublick.config(text=os.path.basename(inputfile))
	
	def OpenPrivateKey(self):
		inputfile = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
													 filetypes =(("PEM File", "*.pem"),("All Files","*.*")),
													 title = "Choose a private key to work"
													 )
		self.labelprivatek.config(text=os.path.basename(inputfile))

	def EncryptnHash(self):
		file=self.labelsf.cget("text")
		publicKey=self.labelpublick.cget("text")
		privateKey=self.labelprivatek.cget("text")
		if not file:
			messagebox.showinfo("Oops!", "Make sure to select a file first!")
		else:
			if not publicKey:
				messagebox.showinfo("Oops!", "Make sure to select the receiver's public key first!")
			else:
				if not privateKey:
					messagebox.showinfo("Oops!", "Make sure to select your private key first!")
				else:
					#HASHING
					try:
						with open(file,'rb') as file_descriptor:	self.file_contents = file_descriptor.read()	
						key = RSA.import_key(open(privateKey).read())
						h = SHA256.new(self.file_contents)
						signature = pkcs1_15.new(key).sign(h)
						delimiter = '\n__sha2_hash_attribute__\n'
						with open(file,'wb')	as file_descriptor:		file_descriptor.write(self.file_contents	+	delimiter.encode()	+	signature)
						print("File Hashed")
						
						#ENCRYPTION
						with open(file,'rb') as file_descriptor:	self.file_contents = file_descriptor.read()	
						outputName="(F-MODE)Encrypted_RSA_AES_"+file
						file_out = open(outputName, "wb")

						recipient_key = RSA.import_key(open(publicKey).read())
						session_key = r.get_random_bytes(16)

						# Encrypt the session key with the public RSA key
						cipher_rsa = PKCS1_OAEP.new(recipient_key)
						enc_session_key = cipher_rsa.encrypt(session_key)

						# Encrypt the data with the AES session key
						cipher_aes = AES.new(session_key, AES.MODE_EAX)
						ciphertext, tag = cipher_aes.encrypt_and_digest(self.file_contents)
						[ file_out.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ]
						messagebox.showinfo("Success", "Message Encrypted and Hashed Successfully")
					except Exception as e:
						messagebox.showinfo("Error", "Something wrong happened...")
						print(e)


	def DecryptnVerify(self):
		file=self.labelsf.cget("text")
		publicKey=self.labelpublick.cget("text")
		privateKey=self.labelprivatek.cget("text")
		delimiter = '\n__sha2_hash_attribute__\n'
		outputName="(F-MODE)Decrypted_RSA_AES_"+file	
		if not file:
			messagebox.showinfo("Oops!", "Make sure to select a file first!")
		else:
			if not publicKey:
				with open(file,'rb') as file_descriptor:	self.file_contents = file_descriptor.read()	
				messagebox.showinfo("Oops!", "Make sure to select the senders's public key first!")
			else:
				if not privateKey:
					messagebox.showinfo("Oops!", "Make sure to select your private key first!")
				else:
					#DECRYPTION
					with open(privateKey, "rb") as priv_key:
						try:
							private_key = RSA.import_key(priv_key.read())
							with open(file,'rb') as file_descriptor:
								enc_session_key, nonce, tag, ciphertext = \
								   [ file_descriptor.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1) ]

							# Decrypt the session key with the private RSA key
							cipher_rsa = PKCS1_OAEP.new(private_key)
							session_key = cipher_rsa.decrypt(enc_session_key)

							# Decrypt the data with the AES session key
							cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
							data = cipher_aes.decrypt_and_verify(ciphertext, tag)
							with open(outputName, "wb") as decrypted_file:
								decrypted_file.write(data)
								print("Message Decrypted Successfully.")
					#HASH VERIFY
							with open(outputName,'rb') as file_descriptor:	self.file_contents = file_descriptor.read()
							try:
								hash_archivo=self.file_contents.split(delimiter.encode(),1)[1]
								contenido=self.file_contents.split(delimiter.encode(),1)[0]
									# print("------------HASH-----------")
									# print(hash_archivo)
									# print("------------contenido-----------")
									# print(contenido)
								key = RSA.import_key(open(publicKey).read())
								h = SHA256.new(contenido)
								try:
									pkcs1_15.new(key).verify(h,hash_archivo)
									messagebox.showinfo("Success", "The file is authentic!")
								except (ValueError, TypeError) as e:
									print(e)
									os.remove(outputName)
									messagebox.showinfo("Warning!", "The hash is incorrect!, try again with a valid key.")
							except IndexError:
								messagebox.showinfo("Warning!", "Your text file doesn't contain a hash")
						except Exception as e:
							messagebox.showinfo("Error", "The decryption process has failed, try again with a valid key.")
							print(e)

class Application(ttk.Frame):
	
	def __init__(self, main_window):
		super().__init__(main_window)
		main_window.title("RSA with AES implementation, by Alejandro Reyes")
		self.main_window = main_window
		main_window.geometry('600x400')
		self.notebook = ttk.Notebook(self)
		
		self.Confidentiality_frame = ConfidentialityFrame(self.notebook)
		self.notebook.add(
			self.Confidentiality_frame, text="Confidentiality Mode", padding=10)
		
		self.Authenticity_frame = AuthenticityFrame(self.notebook)
		self.notebook.add(
			self.Authenticity_frame, text="Authenticity Mode", padding=10)

		self.Full_frame = FullFrame(self.notebook)
		self.notebook.add(
			self.Full_frame, text="Full Mode", padding=10)
		
		self.notebook.pack(padx=0, pady=10)
		self.pack()

main_window = tk.Tk()
app = Application(main_window)
app.mainloop()