from colorama import Fore, Back, Style, init
from cryptography.fernet import Fernet
import sys

init(autoreset=True) # <-Fancy stuff

#PRESENTACIÓN
print(Fore.WHITE +Back.MAGENTA+ Style.BRIGHT +"Cryptography")
print(Fore.WHITE +Back.MAGENTA+ Style.BRIGHT +"Reyes Valenzuela Alejandro - 3CM5")
print(Fore.WHITE +Back.MAGENTA+ Style.BRIGHT +"Implementación del módulo de cifrado simétrico de llave privada Fernet para el cifrado de mensajes en Python")


print(Fore.YELLOW + Style.BRIGHT +"Proceso de cifrado inicializado....")
print(Fore.YELLOW + Style.BRIGHT +"Obteniendo mensaje........")
#Obtenemos el mensaje del primer archivo y lo ciframos
try:
	file = open('m.txt', 'r')
	contenido=file.read()
	file.close()
	print(Fore.GREEN + Style.BRIGHT +"Mensaje obtenido desde archivo m.txt") 
except FileNotFoundError:
	print(Fore.RED + Style.BRIGHT +"Ha ocurrido un error: No se ha podido recuperar el mensaje :(")
	print(Fore.RED + Style.BRIGHT +"Habrá borrado el archivo m.txt?..........") 
	print(Fore.RED+ Style.BRIGHT+"FORZANDO TERMINACIÓN DE PROGRAMA")
	sys.exit()

#Obtenemos una llave generada automáticamente por el módulo Fernet, de la libreria Cryptography
#La variable llave almacenará el valor de una "key" codificada en base64 
llave = Fernet.generate_key()
print(Fore.YELLOW + Style.BRIGHT +"Llave generada")

#Almacena la llave en un archivo determinado
file = open('llaveemisor.txt', 'wb')
file.write(llave)
file.close()

file = open('llavereceptor.txt', 'wb')
file.write(llave)
file.close()
print(Fore.CYAN+ Style.BRIGHT +"Llaves para proceso de comunicación almacenada")

#Ciframos el mensaje usando la llave correspondiente
mensaje= contenido.encode()
f = Fernet(llave)
cifrado = f.encrypt(mensaje)
print(Fore.GREEN+ Style.BRIGHT+"Mensaje cifrado correctamente")

#Guardamos el mensaje cifrado en el nuevo archivo
file = open('c.txt', 'w')
file.write(cifrado.decode())
file.close()
print(Fore.GREEN + Style.BRIGHT+"Mensaje cifrado disponible en archivo c.txt")
print(Fore.CYAN+ Style.BRIGHT+"La ejecución del programa de cifrado ha finalizado correctamente")
print(Fore.CYAN+ Style.BRIGHT+"Ejecute el programa de descifrado para terminar con el proceso de comunicación")