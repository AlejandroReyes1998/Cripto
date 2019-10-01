from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from PIL import Image, ImageFilter  # imports the library

def inv(param):
	number = 256- param;
	inv = 256 - number;
	return inv;
	
def EncryptFile():
		name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
													 filetypes =(("Bitmap File", "*.bmp"),("All Files","*.*")),
													 title = "Choose a file to Encrypt"
													 )

		red = txtr.get()
		green = txtg.get()
		blue = txtb.get()
		txtx=txto.get()
		flag=True
		try:
			int_r=int(red)
			int_g=int(green)
			int_b=int(blue)
			#Comparing with values that are on the Z256 ring
			if((int_r <= 256 and int_r >= 0) and (int_g <= 256 and int_g >= 0) and (int_b <= 256 and int_b >= 0)):
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
				im = Image.open(name)
				print("cool")
				width, height = im.size
				new = Image.new('RGB', (width,height)) # Create a new image
				pixels = new.load()# Load new image descriptor
				for i in range(width):
					for j in range(height): #For every pixel...
					#RGB Treatment using Pillow
						R,G,B = im.getpixel((i,j))  #Get RGB values from the source image and we add the following values
						pixels[i, j] = ((R+int_r)%256,(G+int_g)%256,(B+int_b)%256)
				
				new.save(txtx+".bmp", 'bmp')
				messagebox.showinfo("Success", "Your file has been encrypted successfully")
			except Exception as e:
				print(e)
				print("No file exists")
		else:
			messagebox.showinfo("Error", "Some number is invalid, try again")


#This is where we lauch the file manager bar.
def DecryptFile():

		#Ask for file method retrieved for https://gist.github.com/Yagisanatode/0d1baad4e3a871587ab1
		name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
													 filetypes =(("Bitmap File", "*.bmp"),("All Files","*.*")),
													 title = "Choose a file to Decrypt"
													 )
		red = txtr.get()
		green = txtg.get()
		blue = txtb.get()
		txtx=txto.get()
		flag=True
		try:
			int_r=int(red)
			int_g=int(green)
			int_b=int(blue)
			#Comparing with values that are on the Z256 ring
			if((int_r <= 256 and int_r >= 0) and (int_g <= 256 and int_g >= 0) and (int_b <= 256 and int_b >= 0)):
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
				im = Image.open(name)
				print("cool")
				width, height = im.size
				new = Image.new('RGB', (width,height)) # Create a new image
				pixels = new.load()# Load new image descriptor
				invr=inv(int_r)
				invg=inv(int_g)
				invb=inv(int_b)
				for i in range(width):
					for j in range(height):
						#RGB Treatment using Pillow
						R,G,B = im.getpixel((i,j))  #Adding the inverses to ther respective vector
						pixels[i, j] = ((R+invr)%256,(G+invg)%256,(B+invb)%256)
				
				new.save(txtx+".bmp", 'bmp')
				messagebox.showinfo("Success", "Your file has been decrypted successfully")
			except Exception as e:
				print(e)
				print("No file exists")
		else:
			messagebox.showinfo("Error", "Some number is invalid, try again")

root = Tk()
root.geometry('600x250')
#This code is mine mine mineeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
Title = root.title( "Shift Image Cipher, by Alejandro Reyes")
label = ttk.Label(root, text ="Enter the RGB values to Encrypt/Decrypt your image",foreground="black",font=("Helvetica", 16))
label.pack()
labelr = ttk.Label(root, text ="RED",foreground="red",font=("Helvetica", 16))
labelr.pack()
txtr = Entry(root,width=20)
txtr.pack()
labelg = ttk.Label(root, text ="GREEN",foreground="green",font=("Helvetica", 16))
labelg.pack()
txtg = Entry(root,width=20)
txtg.pack()
labelb = ttk.Label(root, text ="BLUE",foreground="blue",font=("Helvetica", 16))
labelb.pack()
txtb = Entry(root,width=20)
txtb.pack()
labelo = ttk.Label(root, text ="output file",foreground="purple",font=("Helvetica", 16))
labelo.pack()
txto = Entry(root,width=20)
txto.pack()

#Menu Bar
menu = Menu(root)
root.config(menu=menu)
file = Menu(menu)
file.add_command(label = 'Encrypt file', command = EncryptFile)
file.add_command(label = 'Decrypt file', command = DecryptFile)
#this closing program method no tho... (same from open file site :p)
file.add_command(label = 'Exit', command = lambda:exit())
menu.add_cascade(label = 'File', menu = file)
root.mainloop()