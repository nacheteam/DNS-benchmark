#La intención es que se nos diga quién ha sido el mejor DNS con su IP y nombre. También se mantendrá el log de las medias de tiempos de los DNS.
import os                   #Usado para poder llamar a comandos del sistema como ping.
import sys                  #Usado para paso de argumentos.
import subprocess           #Usado para llamar a comandos del sistema
import threading            #Usado para un cerrojo

#Función auxiliar que comprueba si un string se puede convertir en un float.
def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


#Clase DNS. Los resultados finales de la ejecución se guardarán en ips, nombres y medias.
class DNS(object):
    NUM_PAQUETES = 5       #Constate que indica el número de veces que se hará el ping.
    vector_nombres = []
    direcciones_ip = []
    medias_nombres_ips=[]
    errores = []

    cerrojo = threading.Lock()  #Cerrojo para la concurrencia de procesos.
    cerrojo2 = threading.Lock()

    #Lee los nombres y las ips de un archivo con un formato específico "nombre_dns_sin_espacios ip"
    def get_nombres_ip(archivo_dns):
        for ip in archivo_dns:
            nombre = ip[:ip.find(" ")+1]
            DNS.vector_nombres.append(nombre)
            dir_ip = ip[ip.find(" ")+1:len(ip)-1]
            DNS.direcciones_ip.append(dir_ip)

    #Función usada con propósitos de concurrencia. Dado un nombre y una dirección ip testea mediante ping el tiempo de respuesta de dicho servidor.
    #Con dig se comprueba que dicho servidor es capaz de responder querys DNS.
    def get_nombres_medias_ip_Conc(dir_ip, nombre):
        comando_dig = "dig " + dir_ip + " www.ugr.es | head -5 | tail -1"
        dig = subprocess.Popen(['/bin/sh', '-c', comando_dig], stdout=subprocess.PIPE)
        for line in dig.stdout:
            resultado_dig = str(line)
        resultado_dig = resultado_dig[resultado_dig.find(":")+1:]
        resultado_dig = resultado_dig[resultado_dig.find(":")+2:]
        resultado_dig = resultado_dig[:resultado_dig.find(",")]
        if resultado_dig == "NOERROR":

            comando = "ping -c " + str(DNS.NUM_PAQUETES) + " " + dir_ip + "|tail -1"
            process = subprocess.Popen(['/bin/sh', '-c', comando], stdout=subprocess.PIPE)
            resultado=""
            for line in process.stdout:
                resultado = str(line)

            media=0

            if resultado != "\n":
                mitad = resultado[resultado.find("=")+1:]
                aux = mitad[mitad.find("/")+1:]
                media = aux[:aux.find("/")]

            with DNS.cerrojo:
                if isfloat(media):
                    t = (float(media), str(nombre), str(dir_ip))
                    DNS.medias_nombres_ips+=[t]
        else:
            with DNS.cerrojo2:
                DNS.errores.append("Hubo un error con el dns de nombre " + nombre + " y de dirección ip: " + dir_ip + "--->" + resultado_dig)

    #Con el vector de medias final, el de nombre y el de ips la función se encarga de ordenar el vector de medias de menor a mayor y el resto de los vectores se ordenan en consonancia con ello.
    def sort_DNS(medias_nombres_ips):
        medias_nombres_ips.sort()

    #La función elimina los datos de los servidores que han devuelto como tiempo un 0 (no están disponibles).
    def remove_bad_data(medias_nombres_ips):
        while medias_nombres_ips[0][0]==0:
            del medias_nombres_ips[0]
