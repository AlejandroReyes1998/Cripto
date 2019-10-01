from colorama import Fore, Back, Style, init
from cryptography.fernet import Fernet
import sys

init(autoreset=True) # <-Fancy stuff

#PRESENTACIÓN
print(Fore.WHITE +Back.MAGENTA+ Style.BRIGHT +"Cryptography")
print(Fore.WHITE +Back.MAGENTA+ Style.BRIGHT +"Reyes Valenzuela Alejandro - 3CM5")
print(Fore.WHITE +Back.MAGENTA+ Style.BRIGHT +"Implementación del módulo de cifrado simétrico de llave privada Fernet para el descifrado de mensajes en Python")

print(Fore.YELLOW + Style.BRIGHT +"Proceso de descifrado inicializado....")
#Recuperamos la llave para determinar si corresponde al emisor correcto o no
try:
	file = open('llaveemisor.txt', 'rb')
	llave = file.read()
	file.close()
	print(Fore.GREEN + Style.BRIGHT +"Llave para proceso de comunicación del emisor recuperada correctamente, procediendo a recuperar mensaje...")
except FileNotFoundError:
	print(Fore.YELLOW+ Style.BRIGHT +"[ALERTA] Llave extraviada, generando nueva...")
	llave = Fernet.generate_key()
	print(Fore.YELLOW+ Style.BRIGHT+"[ALERTA] Llave generada nuevamente") 
	print(Fore.RED+ Style.BRIGHT+"[ALERTA] Se puede comprometer el contenido del mensaje o la operación de descifrado en general")

#Recuperamos la llave para determinar si corresponde al emisor correcto o no
try:
	file = open('llavereceptor.txt', 'rb')
	llave2 = file.read()
	file.close()
	print(Fore.GREEN + Style.BRIGHT +"Llave para proceso de comunicación del receptor recuperada correctamente, procediendo a recuperar mensaje...")
except FileNotFoundError:
	print(Fore.YELLOW+ Style.BRIGHT +"[ALERTA] Llave extraviada, generando nueva...")
	llave = Fernet.generate_key()
	print(Fore.YELLOW+ Style.BRIGHT+"[ALERTA] Llave generada nuevamente") 
	print(Fore.RED+ Style.BRIGHT+"[ALERTA] Se puede comprometer el contenido del mensaje o la operación de descifrado en general")

#Comparamos ambas llaves para asegurarnos de que el emisor sea el correcto
if(llave!=llave2):
	print(Fore.RED+ Style.BRIGHT+"Ha ocurrido un error: Las llaves no han coincidido y por ende, el emisor puede ser incorrecto :(")
	print(Fore.RED+ Style.BRIGHT+"Se debe de reiniciar el proceso de comunicación :(")
	print(Fore.RED+ Style.BRIGHT+"FORZANDO TERMINACIÓN DE PROGRAMA")
	sys.exit()
else:
	print(Fore.GREEN+ Style.BRIGHT+"Las llaves para el proceso de comunicación han coincidido! :)")

#Recuperamos el mensaje cifrado
print(Fore.YELLOW+ Style.BRIGHT+"Recuperando mensaje....")
try:
	file = open('c.txt', 'r')
	contenido=file.read()
	file.close()
	print(Fore.GREEN+ Style.BRIGHT+"Mensaje cifrado recuperado")
except FileNotFoundError:
	print(Fore.RED+ Style.BRIGHT+"Ha ocurrido un error: No se ha podido recuperar el mensaje :(")
	print(Fore.RED+ Style.BRIGHT+"Intente ejecutar el programa de cifrado primero...")
	print(Fore.RED+ Style.BRIGHT+"FORZANDO TERMINACIÓN DE PROGRAMA")
	sys.exit()

#Con base a la llave generada previamente, desciframos el contenido del archivo y el contenido lo guardamos
f = Fernet(llave2)
try:
	#Las llaves coinciden...
	descifrado= f.decrypt(contenido.encode())
	file = open('mfinal.txt', 'w')
	file.write(descifrado.decode())
	print(Fore.GREEN+ Style.BRIGHT+"Las llaves han coincidido :D")
	file.close()
	print(Fore.GREEN+ Style.BRIGHT+"Mensaje descifrado disponible en archivo mfinal.txt")	
except:
	#Las llaves no coinciden...
	print(Fore.RED+ Style.BRIGHT+"Ha ocurrido un error: Las llaves no han coincidido y por ende, el mensaje no pudo descifrarse :(")
	print(Fore.RED+ Style.BRIGHT+"Se debe de reiniciar el proceso de comunicación :(")
	print(Fore.RED+ Style.BRIGHT+"FORZANDO TERMINACIÓN DE PROGRAMA")
	sys.exit()

print(Fore.CYAN+ Style.BRIGHT+"La ejecución del programa de descifrado ha finalizado correctamente")