#input a,n  tal que gcd(a,n)=1
#output a^-1   
#show all EEA process
#1=ax+ny
#if a^-1 doesn't exist ask for a different a
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def xgcd(a, n):
	"""return (g, x, y) such that a*x + n*y = g = gcd(a, n)"""
	x0, x1, y0, y1 = 0, 1, 1, 0
	rootx = Tk()
	S = Scrollbar(rootx)
	titleaux = rootx.title("Procedure")
	T = Text(rootx, height=70, width=70)
	S.pack(side=RIGHT, fill=Y)
	T.pack(side=LEFT, fill=Y)
	S.config(command=T.yview)
	T.config(yscrollcommand=S.set)
	T.insert(END, "a = "+str(a)+"\n")
	T.insert(END, "n = "+str(n)+"\n")
	print("a = "+str(a))
	print("n = "+str(n))
	T.insert(END, "Obtaining GCD...\n")
	print("Obtaining GCD...")
	strings=[]
	x0s , x1s ,y0s , y1s =[],[],[],[]
	while a != 0:
		aux=n
		quotient, n, a = n // a, a, n % a
		#print("quotient = "+str(quotient)+"  n = "+str(n)+"  a = "+str(a))
		print(str(aux)+" = "+str(n)+"("+str(quotient)+") + "+str(a))
		T.insert(END, str(a)+" = "+str(aux)+" - "+str(n)+"("+str(quotient)+")\n")
		strings.append(str(a)+" = "+str(aux)+" - "+str(n)+"("+str(quotient)+")")
		y0, y1 = y1, y0 - quotient * y1
		y0s.append(y0)
		y1s.append(y1)
		#print("y0 = "+str(y0)+"  y1 = "+str(y1))
		x0, x1 = x1, x0 - quotient * x1
		#print("x0 = "+str(y0)+"  x1 = "+str(y1))
		x0s.append(x0)
		x1s.append(x1)
	#print("Yes, we are :)")
	T.insert(END, "Resulting Equations: \n")
	print("Resulting Equations: ")
	num=1
	for x in strings:
		T.insert(END, str(num)+")"+x+"\n")
		print(str(num)+") "+x)
		num=num+1
	print("Finding a^-1")
	T.insert(END, "Finding a^-1\n")
	#print(strings[-2])
	print("x0")
	print(x0s)
	print("y0")
	print(y0s)
	print("x1")
	print(x1s)
	print("y1")
	print(y1s)
	T.insert(END, "Values for x\n")
	num=0
	for xu in x1s:
		T.insert(END, str(num)+")"+str(xu)+"\n")
		#print(str(num)+") "+xu)
		num=num+1
	T.insert(END, "Values for y\n")
	num=0
	for yu in y1s:
		T.insert(END, str(num)+")"+str(yu)+"\n")
		#print(str(num)+") "+xu)
		num=num+1
	if n == 1:
		#Success
		#T.insert(END, "1 = "+str()"\n")
		T.insert(END, "1 = "+str(abs(y1s[-3]))+"*("+str(abs(x1s[-2]))+") - " +str(abs(x1s[-3]))+"*("+str(abs(y1s[-2]))+")\n")
		T.insert(END, "1 = "+str(abs(y1s[-1]))+"*("+str(abs(x1s[-2]))+") - " +str(abs(x1s[-1]))+"*("+str(abs(y1s[-2]))+")\n")
		T.insert(END, "The equation a*x + n*y = g = gcd(a, n) is satisfied \n")
		T.insert(END, "GCD == 1, therefore, a^-1 exists.\n")
		T.insert(END, "a^-1 = "+str(x0s[-1])+"\n")
	else:
		#Failure
		T.insert(END, "GCD != 1, therefore, a^-1 doesn't exists.\n")
	#rootx.mainloop()
	return n, x0, y0

def mulinv(a, n):
	"""return x such that (x * a) % n == 1"""
	print("Begining Algorithm")
	g, x, y = xgcd(a, n)
	print("g="+str(g))
	print("x="+str(g))
	print("y="+str(g))
	if g == 1:
		messagebox.showinfo("Success", "These numbers are coprimes, so, a^-1 exists and it is equal to: "+str(x % n))
		return x % n
	else:4
		messagebox.showinfo("Yikes", "These numbers aren't coprimes, Ask for another number...")
		return 0
	
def Validate():
	the_a = txta.get()
	the_n = txtn.get()
	flag=True
	try:
		int_a=int(the_a)
		int_n=int(the_n)
	except:
		print("not a number m8")
		flag=False
	if(flag):
		print("Yeah")
		#inv=inverse(int_a, int_n)
		inv=mulinv(int_a, int_n)
		if(inv==0):
			print("Inverse doesn't exist")
		else:
			print(inv)
	else:
		messagebox.showinfo("Error", "Some number is invalid, try again")

if __name__ == "__main__":
	root = Tk()
	root.geometry('600x175')
	#This code is mine mine mineeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
	Title = root.title( "Euclidean Extended Algorithm Implementation, by Alejandro Reyes")
	label = ttk.Label(root, text ="Insert a and n such that gcd(a,n)=1",foreground="black",font=("Helvetica", 16))
	label.pack()
	labela = ttk.Label(root, text ="Number 'a'",foreground="blue",font=("Segoe UI", 16))
	labela.pack()
	txta = Entry(root,width=20)
	txta.pack()
	labeln = ttk.Label(root, text ="Number 'n'",foreground="blue",font=("Segoe UI", 16))
	labeln.pack()
	txtn = Entry(root,width=20)
	txtn.pack()
	calculate = ttk.Button(root, text="Calculate", command=Validate)
	calculate.pack()

	#Menu Bar
	menu = Menu(root)
	root.config(menu=menu)
	file = Menu(menu)
	#this closing program method no tho... (same from open file site :p)
	file.add_command(label = 'Exit', command = lambda:exit())
	menu.add_cascade(label = 'Options', menu = file)
	root.mainloop()