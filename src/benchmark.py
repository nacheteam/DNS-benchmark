from best_dns import DNS        #Importo la clase de DNS definida en best_dns.py
import os                       #Usado para mandar comandos al sistema.
import sys                      #Usado para los argumentos del programa
import threading                #Usado para la concurrencia
import time                     #Usado para la medición de tiempos
import subprocess           #Usado para llamar a comandos del sistema


os.system("clear")
NUM_MAX_HEBRAS = input("Introduzca el número de hebras que quiere usar de manera concurrente: ")
NUM_MAX_HEBRAS = int(NUM_MAX_HEBRAS)

os.system("rm error_log.txt")
os.system("touch error_log.txt")

total_time_init = time.time()

#Obtengo los nombres e ips de los dns pasados como argumento al programa.
archivo_dns = open(sys.argv[1], "r")
os.system("clear")
print("Comenzando el ping a los candidatos DNS...")
DNS.get_nombres_ip(archivo_dns)
archivo_dns.close()

#Utilizo la concurrencia para crear hebras que calculen en paralelo la velocidad de cada servidor.
n=len(DNS.vector_nombres)
num_hebras=0
print("Comenzando las tandas de pings!")
while num_hebras<n:
    start = time.time()
    hebras = []
    if n-num_hebras>NUM_MAX_HEBRAS:
        maxim=NUM_MAX_HEBRAS
    else:
        maxim = n-num_hebras
    print("Analizando del servidor " + str(num_hebras) + " al servidor " + str(num_hebras+maxim))
    for i in range(0,maxim):
        hebras.append(threading.Thread(target=DNS.get_nombres_medias_ip_Conc, args=(DNS.direcciones_ip[num_hebras+i], DNS.vector_nombres[num_hebras+i])))
    for i in range(0,maxim):
        hebras[i].start()
    for i in range(0,maxim):
        hebras[i].join()
    num_hebras+=maxim
    end = time.time()
    print("La tanda ha tardado " + str(end-start) + " segundos.")


#Una vez calculados los datos de velocidad para cada servidor ordeno dichos datos y elimino los datos erroneos.
os.system("clear")
print("Obteniendo el mejor resultado...")
DNS.sort_DNS(DNS.medias, DNS.nombres, DNS.ips)
DNS.remove_bad_data(DNS.medias, DNS.nombres, DNS.ips)

#Doy finalmente los resultados obtenidos.
total_time_end = time.time()
os.system("clear")
print(str(n) + " servidores DNS han sido analizados.")
print("El mejor dns ha sido " + DNS.nombres[0] + "-->" + DNS.ips[0] + " con una media de tiempo de " + str(DNS.medias[0]) + " ms")
os.system("rm -rf __pycache__/")
print("Ha tardado en total " + str(total_time_end-total_time_init) + " segundos.")

error_file = open("error_log.txt", "r+")
for element in DNS.errores:
    error_file.write(element)

print("Fin de creación del log de erorres")
