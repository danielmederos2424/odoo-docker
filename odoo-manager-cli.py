#!/usr/bin/env python3

import os
import time
import subprocess
import logging
from datetime import datetime


# Configuración del sistema de logs
logging.basicConfig(filename='odoo_instance_manager.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# cambiar print por logging.info


# Funciones auxiliares
def limpiar_consola():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')


def obtener_directorio():
    dir = os.getcwd()
    return dir


def obtener_instancia():
    dir = obtener_directorio()
    odoo_folder = f"{dir}/odoo"
    num_instancia = 0 
    conf_files = [f for f in os.listdir(odoo_folder) if f.startswith("odoo") and f.endswith(".conf")]
    for conf_file in conf_files:
        number = conf_file[4:-5]
        if number.isdigit() and int(number) > num_instancia:
            num_instancia = int(number)
    
    return num_instancia


def obtener_edicion(version_odoo):
    while True:
        print(f"Seleccione la edición de Odoo {version_odoo} que desea instalar:")
        print("[1] Community")
        print("[2] Enterprise")
        opcion = input(">> ")

        if opcion == "1":
            edicion = "community"
            break
        elif opcion == "2":
            edicion = "enterprise"
            break
        else:
            limpiar_consola()
            input("Opción no válida, intente otra vez...")
    
    return edicion
 
 
def crear_conf(dir,instancia, dbfilter, nombre_instancia, version, edicion, password):
    conf_text = "[options]\n"
    conf_text += "addons_path = /mnt/extra-addons"
    if edicion == "enterprise":
        conf_text += f", /mnt/extra-addons2"
    conf_text += "\n"
    conf_text += "data_dir = /var/lib/odoo\n"
    conf_text += f"admin_passwd = {password}\n"
    if dbfilter == False:
        conf_text += ";"
    conf_text += f"dbfilter = ^(.*)odoo{version}_{edicion}{nombre_instancia}$\n"
    conf_text += "db_host = postgres_db\n"
    conf_text += "db_password = pgOd0op4sswOrd\n"
    conf_text += "db_port = 5432\n"
    conf_text += ";db_sslmode = prefer\n"
    conf_text += "db_template = template0\n"
    conf_text += "db_user = pgodoouser\n"
    conf_text += "list_db = True\n"
    conf_text += "proxy_mode = False\n"

    with open(f"{dir}/odoo/odoo{instancia}.conf", "w") as conf_file:
        conf_file.write(conf_text)


# Funciones de verificacion
def crear_network():
    limpiar_consola()
    print(">>>> Sistema de gestión de instancias múltiples de Odoo <<<<")
    time.sleep(1)
    print("Realizando verificaciones iniciales...")
    time.sleep(1)
    print("Verificando la existencia de la red 'odoo-network'...")
    time.sleep(1)
    try:
        cmd_networks = "docker network ls --format '{{.Name}}'"
        networks = subprocess.check_output(cmd_networks, shell=True, text=True).splitlines()

        if 'odoo-network' in networks:
            print("odoo-network existe.")
        else:
            print("odoo-network no existe. Creando...")
            cmd_create = "docker network create odoo-network"
            subprocess.run(cmd_create, shell=True)
            
        time.sleep(1)
        
        verificar_postgres()

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        input()
        exit()


def verificar_postgres():
    print("Verificando el contenedor de postgres...")
    time.sleep(1)
    try:
        cmd_status = "docker inspect -f '{{.State.Status}}' postgres_db"
        status = subprocess.check_output(cmd_status, shell=True, text=True).strip()

        if status == 'running':
            print("El contenedor de postgres se encuentra activo.")
            time.sleep(1)
        elif status == 'exited':
            print("El contenedor de postgres se encuentra detenido. Reiniciando...")
            cmd_restart = "docker restart postgres_db"
            subprocess.run(cmd_restart, shell=True)
            time.sleep(1)
        else:
            print(f"Unexpected status: {status}")
            time.sleep(1)
    except subprocess.CalledProcessError:
        print("Creando contenedor de postgres...")
        cmd_create = ("docker run -d --name postgres_db --restart=unless-stopped --network=odoo-network -v pg_data:/var/lib/postgresql/data:rw -e POSTGRES_USER=pgodoouser -e POSTGRES_PASSWORD=pgOd0op4sswOrd -e POSTGRES_DB=postgres postgres:15")
        subprocess.run(cmd_create, shell=True)
        time.sleep(1)

    print("Contenedor de postgres verificado con éxito.")
    time.sleep(2)
    menu_principal()


# Crear instancias de Odoo
def crear_instancia(version, instancia, puerto, dir):
    limpiar_consola()
    
    print(f">>>> Crear una nueva instancia de Odoo {version} <<<<")
    edicion = obtener_edicion(version)
    
    if edicion == "community":
        ent_addons = ""
    elif edicion == "enterprise":
        ent_addons = f"-v {dir}/odoo/ent_addons/{version}:/mnt/extra-addons2:rw "
    
    limpiar_consola()
    entrada = input("Especifique el nombre de la instancia (dejar en blanco si para no especificar):")
    if entrada == "":
        nombre_instancia = entrada
    else:
        nombre_instancia = "_"+str(entrada)
    
    while True:
        password = input("Ingrese la contraseña de administrador de la instancia: ")
        if password != "":
            break
        else:
            limpiar_consola()
            input("La contraseña no puede estar en blanco, intente otra vez...")
    
    limpiar_consola()
    while True:
        print("Desearía filtrar la base de datos?")
        print("[1] Sí")
        print("[2] No") 
        opcion = input(">> ")
        if opcion == "1":
            dbfilter = True
            break
        elif opcion == "2":
            dbfilter = False
            break
        else:
            limpiar_consola()
            input("Opción incorrecta, intente otra vez...")
                
    crear_conf(dir, instancia, dbfilter, nombre_instancia, version, edicion, password)
            
    limpiar_consola()
    print("Creando instancia de Odoo...")
    os.system(f"docker run -d --name odoo{instancia}_{version}{edicion}{nombre_instancia} --restart=unless-stopped --network=odoo-network -p {puerto}:8069 -v odoo_data:/var/lib/odoo:rw -v {dir}/odoo/odoo{instancia}.conf:/etc/odoo/odoo.conf -v {dir}/odoo/odoo{instancia}_addons:/mnt/extra-addons:rw {ent_addons}odoo:{version}")
    
    
    print("Instancia creada con éxito.")
    print(f"""
    >>> Información de la instancia <<<
    Nombre: odoo{instancia}_{version}{edicion}{nombre_instancia}
    Puerto: {puerto}
    Versión: {version}
    Edición: {edicion}
    Contraseña de administrador: {password}
    En caso de haber habilitado dbfilter, revisar en archivo de configuración.      
    """)
    input("Presione Enter para continuar...")


# Menús
def nueva_instancia():
    num_instancia = obtener_instancia()
    instancia = num_instancia + 1
    puerto = 8069 + num_instancia
    dir = obtener_directorio()
    
    while True:
        limpiar_consola()
        print(">>>> Crear una nueva instancia de Odoo <<<<")
        print(f"Instancias de Odoo existentes: {num_instancia}")
        print("Seleccione la versión de Odoo que desea instalar:")
        print("[1] Odoo 14")
        print("[2] Odoo 15")
        print("[3] Odoo 16")
        print("[4] Odoo 17")
        print("[0] Volver al menú principal")

        opcion = input(">> ")

        if opcion == "1":
            version = "14"
            break
        elif opcion == "2":
            version = "15"
            break
        elif opcion == "3":
            version = "16"
            break
        elif opcion == "4":
            version = "17"
            break
        elif opcion == "0":
            break
        else:
            limpiar_consola()
            input("Opción no válida, intente otra vez...")

    crear_instancia(version, instancia, puerto, dir)


def modificar_instancia(accion, comando):
    limpiar_consola()
    os.system("docker ps -a")
    instancia = input(f"\nIndique el nombre de la instancia a {accion}: ")
    try:
        limpiar_consola()
        if comando == "rm":
            os.system(f"docker stop {instancia} && docker {comando} {instancia}")
        else:    
            os.system(f"docker {comando} {instancia}")
        if comando != "logs":
            print(f"Estado de la instancia {instancia} modificado con éxito ({accion})")
    except Exception as e:
        print(f"Error al {accion} la instancia: {e}")
    input("Presione Enter para volver al menú principal...")


def ver_instancias():
    limpiar_consola()
    while True:
        print(">>>> Información sobre los contenedores existentes <<<<")
        os.system("docker ps -a")
        print("\n>>> Qué desea hacer? <<<")
        print("[1] Detener una instancia")
        print("[2] Eliminar una instancia")
        print("[3] Ver logs de una instancia")
        print("[4] Reiniciar una instancia")
        print("[0] Volver al menú principal")

        opcion = input(">> ")
        if opcion == "1":
            comando = "stop"
            accion = "detener"
            modificar_instancia(accion, comando)
            break
        elif opcion == "2":
            comando = "rm"
            accion = "eliminar"
            modificar_instancia(accion, comando)
            break
        elif opcion == "3":
            comando = "logs"
            accion = "ver los logs de"
            modificar_instancia(accion, comando)
            break            
        elif opcion == "4":
            comando = "restart"
            accion = "reiniciar"
            modificar_instancia(accion, comando)
            break
        elif opcion == "0":
            break


def mostrar_ayuda():
    limpiar_consola()
    print(""">>> Información sobre el programa <<<
El presente programa permite crear, modificar, reiniciar, monitorizar y eliminar instancias de Odoo en contenedores Docker. Para volver a poner en ejecución una instancia detenida, ingrese al submenú " Ver instancias existentes" y reinicie aquella instancia deseada. Asimismo pueden ser detenidas aquellas instancias que ya no sean necesarias dentro de dicho submenu.        
""")
    input("Pulse Enter para volver al Menú Principal...")
    menu_principal()


def menu_principal():
    while True:
        limpiar_consola()
        print(">>>> Sistema de gestión de instancias múltiples de Odoo <<<<")
        print("[1] Crear una nueva instancia de Odoo")
        print("[2] Ver instancias existentes")
        print("[3] Ayuda")
        print("[0] Salir")

        opcion = input(">> ")

        if opcion == "1":
            nueva_instancia()
        elif opcion == "2":
            ver_instancias()
        elif opcion == "3":
            mostrar_ayuda()
        elif opcion == "0":
            limpiar_consola()
            print("Saliendo del programa")
            time.sleep(1)
            exit()
        else:
            limpiar_consola()
            input("Opción no válida, intente otra vez...")


if __name__ == "__main__":
    crear_network()
