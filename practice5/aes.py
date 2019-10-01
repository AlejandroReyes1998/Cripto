from tkinter import * #UI stuff
from tkinter import ttk #UI stuff
from tkinter.filedialog import askopenfilename #UI stuff
from tkinter import messagebox #UI stuff
from PIL import Image, ImageFilter #Image treatment
from Crypto.Cipher import AES #AES Algorithm implementation
import os #Play with the filenames

#des module for encrypt/decrypt information
def aesCipher(key,data,mode,function,iv):
	#We don't worry 'bout the initial vector if we are using ECB
	if(mode=='ECB'):		tempCipher = AES.new(toUtf8(padKeyAes(key)), AES.MODE_ECB)
	elif(mode=='CBC'):		tempCipher = AES.new(toUtf8(padKeyAes(key)), AES.MODE_CBC, toUtf8(padIV(iv,'AES')))
	elif(mode=='OFB'):		tempCipher = AES.new(toUtf8(padKeyAes(key)), AES.MODE_OFB, toUtf8(padIV(iv,'AES')))
	elif(mode=='CFB'):		tempCipher = AES.new(toUtf8(padKeyAes(key)), AES.MODE_CFB, toUtf8(padIV(iv,'AES')))
	elif(mode=='CTR'):		tempCipher = AES.new(toUtf8(padKeyAes(key)), AES.MODE_CTR,nonce=b'', initial_value=toUtf8(padIV(iv,'AES')))
	return tempCipher.encrypt(pad(data,'AES'))	if (function=='Encrypt') else  tempCipher.decrypt(pad(data,'AES'))

#encodes in order to be able to use the library functions
def toUtf8(data):	return data.encode('UTF-8')

#Adds or deletes 0's to fullfil the 8bit multiplier
def padKeyAes(key):
	paddedKey = pad(key.encode(),'AES').decode()
	if(len(paddedKey) not in [16,24,32]):
		messagebox.showinfo("Warning!","Key too long. Padding key with size: "+str(len(paddedKey)))
		if(len(paddedKey)>32):	return paddedKey[:32]
		if(len(paddedKey)>24):	return paddedKey[:24]
		if(len(paddedKey)>16):	return paddedKey[:16]
	return pad(key.encode(),'AES').decode()

#The same but for the IV
def padIV(iv,mode):
	padded_IV = pad(iv.encode(),mode).decode()
	if(mode=='AES' and len(padded_IV)>AES.block_size):	return padded_IV[:AES.block_size]
	return padded_IV

#Fullfill the block if the data isn't large enough
def pad(data,mode):
	length	=	(AES.block_size - len(data)) % AES.block_size
	return	data + bytes([length])*length

#Valid key?
def Validate():
	fun=comboe.get()
	mode=comboec.get()
	key=txtk.get()
	iv=txtiv.get()
	flag=True
	try:
		int_k=int(key)
		print("cool")
	except:
		flag=False
		print("Not a number m8")

	#The key is valid, but we have yet another value to check..........	
	if(flag):
		#Anyway,we don't use the IV on ECB
		if(mode=='ECB'):
			if(fun=='Encrypt'):
				print("Encrypt mode")
				EncryptFile(mode,key,iv)
			else:
				print("Decrypt mode")
				DecryptFile(mode,key,iv)
		else:
			#Valid IV?
			if not iv.strip():
				messagebox.showinfo("Error", "The Initial Vector for "+mode+"-mode is invalid, try again")
			else:
				if(fun=='Encrypt'):
					print("Encrypt mode")
					EncryptFile(mode,key,iv)
				else:
					print("Decrypt mode")
					DecryptFile(mode,key,iv)
	else:
		messagebox.showinfo("Error", "The 8-bit key is invalid, try again")

#Encrypt image
def EncryptFile(mode,key,iv):
		name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
													 filetypes =(("Bitmap File", "*.bmp"),("All Files","*.*")),
													 title = "Choose a file to Encrypt"
													 )
		#We convert the image into a byte array (rgb values)
		image = Image.open(name).convert('RGB')
		image_array	= bytes(image.tobytes())
		#Obtaining the filename
		filename_w_ext = os.path.basename(name)
		filename, file_extension = os.path.splitext(filename_w_ext)
		print(mode)
		image_array =  aesCipher(key,image_array,mode,'Encrypt',iv)
		#We save the new image
		Image.frombytes("RGB", image.size, image_array, "raw", "RGB").save("encrypt"+"_"+filename+"_"+mode+".bmp",format='BMP')

		messagebox.showinfo("Success","Your file has been encrypted with AES-"+mode+" mode succesfully!")
#Encrypt image
def DecryptFile(mode,key,iv):

		#Ask for file method retrieved for https://gist.github.com/Yagisanatode/0d1baad4e3a871587ab1
		name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
													 filetypes =(("Bitmap File", "*.bmp"),("All Files","*.*")),
													 title = "Choose a file to Decrypt"
													 )
		#We convert the image into a byte array (rgb values)
		image = Image.open(name).convert('RGB')
		image_array	= bytes(image.tobytes())
		#Obtaining the filename
		filename_w_ext = os.path.basename(name)
		filename, file_extension = os.path.splitext(filename_w_ext)
		#If the file was encrypted using our program, we split the filename to obtain the original
		slash=filename.split("_")
		print(slash)
		print(len(slash))
		x=""
		if(len(slash)>1):
			x=slash[1]
		else:
			x=slash[0]
		print(mode)
		image_array =  aesCipher(key,image_array,mode,'Decrypt',iv)
		#We save the new image
		Image.frombytes("RGB", image.size, image_array, "raw", "RGB").save("decrypt"+"_"+x+"_"+mode+".bmp",format='BMP')
		messagebox.showinfo("Success","Your file has been Decrypted with AES-"+mode+" mode succesfully!")

if __name__ == "__main__":
	root = Tk()
	root.geometry('600x300')
	#This code is mine mine mineeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
	Title = root.title( "AES Operation Modes, by Alejandro Reyes")
	label = ttk.Label(root, text ="Enter the key and the initial vector (if necesary) to Encrypt/Decrypt your image",foreground="black",font=("Helvetica", 10))
	label.pack()
	labelk = ttk.Label(root, text ="Key",foreground="blue",font=("Segoe UI", 16))
	labelk.pack()
	txtk = Entry(root,width=20)
	txtk.pack()
	labeliv = ttk.Label(root, text ="Initial Vector (if necesary)",foreground="blue",font=("Segoe UI", 16))
	labeliv.pack()
	txtiv = Entry(root,width=20)
	txtiv.pack()
	labele = ttk.Label(root, text ="Encrypt/Decrypt mode",foreground="blue",font=("Segoe UI", 16))
	labele.pack()
	comboe = ttk.Combobox(root, state="readonly")
	comboe["values"] = ["Encrypt", "Decrypt"]
	comboe.current(0)
	comboe.pack()
	labelec = ttk.Label(root, text ="Operation Mode",foreground="blue",font=("Segoe UI", 16))
	labelec.pack()
	comboec = ttk.Combobox(root, state="readonly")
	comboec["values"] = ["ECB", "CBC","CFB","OFB","CTR"]
	comboec.current(0)
	comboec.pack()
	startbutton = ttk.Button(root, text="Start!", command=Validate)
	startbutton.pack()

	#Menu Bar
	menu = Menu(root)
	root.config(menu=menu)
	file = Menu(menu)
	#this closing program method no tho... (same from open file site :p)
	file.add_command(label = 'Exit', command = lambda:exit())
	menu.add_cascade(label = 'Options', menu = file)
	root.mainloop()