from best_dns import DNS        #Importo la clase de DNS definida en best_dns.py
import os                       #Usado para mandar comandos al sistema.
import sys                      #Usado para los argumentos del programa
import threading                #Usado para la concurrencia
import time                     #Usado para la medición de tiempos
import subprocess           #Usado para llamar a comandos del sistema

class Main(object):
    NUM_MAX_HEBRAS=0

    #Función que pide al usuario el número de hebras que quiere que se utilicen.
    def begining_function():
        os.system("clear")
        os.system("rm error_log.txt 2> /dev/null")
        os.system("touch error_log.txt")
        Main.NUM_MAX_HEBRAS = input("Introduzca el número de hebras que quiere usar de manera concurrente: ")
        Main.NUM_MAX_HEBRAS = int(Main.NUM_MAX_HEBRAS)

    #Lee los nombres del fichero de DNS.
    def get_names():
        archivo_dns = open(sys.argv[1], "r")
        os.system("clear")
        DNS.get_nombres_ip(archivo_dns)
        archivo_dns.close()

    #Función que se encarga del multithreading.
    def pinging_function():
        n=len(DNS.vector_nombres)
        num_hebras=0
        while num_hebras<n:
            start = time.time()
            hebras = []
            if n-num_hebras>Main.NUM_MAX_HEBRAS:
                maxim=Main.NUM_MAX_HEBRAS
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

    #Encuentra el mejor resultado de los obtenidos en el ping.
    def find_best_result():
        os.system("clear")
        DNS.sort_DNS(DNS.medias_nombres_ips)
        DNS.remove_bad_data(DNS.medias_nombres_ips)

    #Da el mejor resultado encontrado.
    def give_best_result():
        n=len(DNS.vector_nombres)
        os.system("clear")
        print(str(n) + " servidores DNS han sido analizados.")
        print("El mejor dns ha sido " + DNS.medias_nombres_ips[0][1] + "-->" + DNS.medias_nombres_ips[0][2] + " con peor tiempo de " + str(DNS.medias_nombres_ips[0][0]) + " ms para querys.")
        print("Su media de ping es: " + str(DNS.medias_nombres_ips[0][3]) + " ms")
        os.system("rm -rf __pycache__/")

    #Escribe los errores encontrados en un fichero externo.
    def create_error_log():
        if len(DNS.errores)==0:
            os.system("rm error_log.txt")
            print("No hubo errores.")
        else:
            error_file = open("error_log.txt", "r+")
            for element in DNS.errores:
                error_file.write(element)
            print("Fin de creación del log de erorres")
            error_file.close()

    #Función a ejecutar para llevar a cabo el programa.
    def main():
        start = time.time()
        Main.begining_function()
        print("Comenzando la obtención de servidores...")
        Main.get_names()
        print("Benchmark en progreso, " + str(len(DNS.vector_nombres)) + " han sido encontrados en el fichero.")
        Main.pinging_function()
        print("Obteniendo el mejor resultado...")
        Main.find_best_result()
        Main.give_best_result()
        Main.create_error_log()
        end = time.time()
        print("En total ha tardado " + str(end-start) + " segundos.")
        print("Las webs usadas han sido:")
        for web in DNS.testing_webs:
            print(web)
        print("Fin de creación del log de erorres")


Main.main()
