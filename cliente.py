import requests
import json
from datetime import datetime

#Url api
URL_BASE = "http://localhost:8000"

# Token para autenticación
with open("token.txt", "r") as f:
    TOKEN = f.read().strip()

# Headers con token
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

#Valida int
def pedir_numero(dato, mensaje_error):
    while True:
        try:
            return int(input(dato))
        except ValueError:
            print(mensaje_error)

#REgistrar logs
def registrar_log(usuario, operacion):
    with open("logs.txt", "a") as archivo:
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log = f"{fecha} | Usuario: {usuario} | Operación: {operacion}\n"
        archivo.write(log)

#Funciones pacinetes
#Alta paciente
def alta_paciente():
    try:
        print("\n--- ALTA DE PACIENTE ---")
        dni = pedir_numero("DNI: ", "Error: el DNI debe ser un número")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        edad = pedir_numero("Edad: ", "Error: la edad debe ser un número")
        telefono = pedir_numero("Teléfono: ", "Error: el teléfono debe ser un número")
        obra_social = input("Obra social: ")
        
        datos = {
            "id": 0,
            "dni": dni,
            "nombre": nombre,
            "apellido": apellido,
            "edad": edad,
            "telefono": telefono,
            "obra_social": obra_social
        }
        
        respuesta = requests.post(f"{URL_BASE}/pacientes", json=datos, headers=HEADERS)
        
        if respuesta.status_code == 200:
            print("Paciente creado exitosamente")
            registrar_log("admin", f"Crear paciente: {nombre} {apellido}")
        else:
            print("Error: revisa los datos cargados")
    except Exception as e:
        print("Error inesperado")

#Listado pcientes
def listar_pacientes():
    try:
        print("\n--- LISTADO DE PACIENTES ---")
        respuesta = requests.get(f"{URL_BASE}/pacientes")
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            pacientes = datos.get("pacientes", [])
            
            if not pacientes:
                print("No hay pacientes registrados")
            else:
                for p in pacientes:
                    print(f"ID: {p['id']} | {p['nombre']} {p['apellido']} | DNI: {p['dni']}")
            registrar_log("admin", "Listar pacientes")
        else:
            print(f"Error al obtener pacientes. Código de estado: {respuesta.status_code}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#Buscar paciente
def buscar_paciente():
    try:
        print("\n--- BUSCAR PACIENTE ---")
        id_paciente = pedir_numero("ID: ", "Error: el ID debe ser un número")
        
        respuesta = requests.get(f"{URL_BASE}/pacientes/{id_paciente}")
        
        if respuesta.status_code == 200:
            p = respuesta.json()["paciente"]
            print(f"\nPaciente encontrado:")
            print(f"ID: {p['id']}")
            print(f"Nombre: {p['nombre']} {p['apellido']}")
            print(f"DNI: {p['dni']}")
            print(f"Edad: {p['edad']}")
            print(f"Teléfono: {p['telefono']}")
            print(f"Obra social: {p['obra_social']}")
            registrar_log("admin", f"Buscar paciente: {id_paciente}")
        else:
            print(f"Paciente no encontrado.Código de estado: {respuesta.status_code}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#modificar paciente
def modificar_paciente():
    try:
        print("\n--- MODIFICAR PACIENTE ---")
        id_paciente = pedir_numero("ID: ", "Error: el ID debe ser un número")
        
        dni = pedir_numero("DNI: ", "Error: el DNI debe ser un número")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        edad = pedir_numero("Edad: ", "Error: la edad debe ser un número")
        telefono = pedir_numero("Teléfono: ", "Error: el teléfono debe ser un número")
        obra_social = input("Obra social: ")
        
        datos = {
            "id": id_paciente,
            "dni": dni,
            "nombre": nombre,
            "apellido": apellido,
            "edad": edad,
            "telefono": telefono,
            "obra_social": obra_social
        }
        
        respuesta = requests.put(f"{URL_BASE}/pacientes/{id_paciente}", json=datos, headers=HEADERS)
        
        if respuesta.status_code == 200:
            print("Paciente actualizado exitosamente")
            registrar_log("admin", f"Modificar paciente: {id_paciente}")
        else:
            print("Error: revisa los datos cargados")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#Eliminar pciente
def eliminar_paciente():
    try:
        print("\n--- ELIMINAR PACIENTE ---")
        id_paciente = pedir_numero("ID: ", "Error: el ID debe ser un número")
        
        confirmacion = input("¿Estás seguro? (s/n): ")
        if confirmacion.lower() != "s":
            print("Operación cancelada")
            return
        
        respuesta = requests.delete(f"{URL_BASE}/pacientes/{id_paciente}", headers=HEADERS)
        
        if respuesta.status_code == 200:
            print("Paciente eliminado exitosamente")
            registrar_log("admin", f"Eliminar paciente: {id_paciente}")
        else:
            print("Error al eliminar el paciente")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#Menu pacientes
def menu_pacientes():
    while True:
        print("\n--- GESTIONAR PACIENTES ---")
        print("1 - Alta paciente")
        print("2 - Buscar paciente")
        print("3 - Modificar paciente")
        print("4 - Eliminar paciente")
        print("5 - Listar pacientes")
        print("6 - Volver")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            alta_paciente()
        elif opcion == "2":
            buscar_paciente()
        elif opcion == "3":
            modificar_paciente()
        elif opcion == "4":
            eliminar_paciente()
        elif opcion == "5":
            listar_pacientes()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")

#Funciones medicos
#Alta medico
def alta_medico():
    try:
        print("\n--- ALTA DE MÉDICO ---")
        matricula = pedir_numero("Matrícula: ", "Error: la matrícula debe ser un número")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        especialidad = input("Especialidad: ")
        telefono = pedir_numero("Teléfono: ", "Error: el teléfono debe ser un número")
        
        datos = {
            "id": 0,
            "matricula": matricula,
            "nombre": nombre,
            "apellido": apellido,
            "especialidad": especialidad,
            "telefono": telefono
        }
        
        respuesta = requests.post(f"{URL_BASE}/medicos", json=datos, headers=HEADERS)
        
        if respuesta.status_code == 200:
            print("Médico creado exitosamente")
            registrar_log("admin", f"Crear médico: {nombre} {apellido}")
        else:
            print("Error: revisa los datos cargados")
    except Exception as e:
        print("Ocurrió un error inesperado")

#Listar medicocs
def listar_medicos():
    try:
        print("\n--- LISTADO DE MÉDICOS ---")
        respuesta = requests.get(f"{URL_BASE}/medicos")
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            medicos = datos.get("medicos", [])
            
            if not medicos:
                print("No hay médicos registrados")
            else:
                for m in medicos:
                    print(f"ID: {m['id']} | {m['nombre']} {m['apellido']} | Especialidad: {m['especialidad']}")
            registrar_log("admin", "Listar médicos")
        else:
            print(f"Error al obtener médicos. Código de estado: {respuesta.status_code}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#Buecar medico
def buscar_medico():
    try:
        print("\n--- BUSCAR MÉDICO ---")
        id_medico = pedir_numero("ID: ", "Error: el ID debe ser un número")
        
        respuesta = requests.get(f"{URL_BASE}/medicos/{id_medico}")
        
        if respuesta.status_code == 200:
            m = respuesta.json()["medico"]
            print(f"\nMédico encontrado:")
            print(f"ID: {m['id']}")
            print(f"Nombre: {m['nombre']} {m['apellido']}")
            print(f"Matrícula: {m['matricula']}")
            print(f"Especialidad: {m['especialidad']}")
            print(f"Teléfono: {m['telefono']}")
            registrar_log("admin", f"Buscar médico: {id_medico}")
        else:
            print(f"Médico no encontrado. Código de estado: {respuesta.status_code}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#Modificar medico
def modificar_medico():
    try:
        print("\n--- MODIFICAR MÉDICO ---")
        id_medico = pedir_numero("ID: ", "Error: el ID debe ser un número")
        
        matricula = pedir_numero("Matrícula: ", "Error: la matrícula debe ser un número")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        especialidad = input("Especialidad: ")
        telefono = pedir_numero("Teléfono: ", "Error: el teléfono debe ser un número")
        
        datos = {
            "id": id_medico,
            "matricula": matricula,
            "nombre": nombre,
            "apellido": apellido,
            "especialidad": especialidad,
            "telefono": telefono
        }
        
        respuesta = requests.put(f"{URL_BASE}/medicos/{id_medico}", json=datos, headers=HEADERS)
        
        if respuesta.status_code == 200:
            print("Médico actualizado exitosamente")
            registrar_log("admin", f"Modificar médico: {id_medico}")
        else:
            print("Error: revisa los datos cargados")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#eliminar medico
def eliminar_medico():
    try:
        print("\n--- ELIMINAR MÉDICO ---")
        id_medico = pedir_numero("ID: ", "Error: el ID debe ser un número")

        confirmacion = input("¿Estás seguro? (s/n): ")
        if confirmacion.lower() != "s":
            print("Operación cancelada")
            return
        
        respuesta = requests.delete(f"{URL_BASE}/medicos/{id_medico}", headers=HEADERS)
        
        if respuesta.status_code == 200:
            print("Médico eliminado exitosamente")
            registrar_log("admin", f"Eliminar médico: {id_medico}")
        else:
            print("Error al eliminar el médico")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#Menu medicos
def menu_medicos():
    while True:
        print("\n--- GESTIONAR MÉDICOS ---")
        print("1 - Alta médico")
        print("2 - Buscar médico")
        print("3 - Modificar médico")
        print("4 - Eliminar médico")
        print("5 - Listar médicos")
        print("6 - Volver")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            alta_medico()
        elif opcion == "2":
            buscar_medico()
        elif opcion == "3":
            modificar_medico()
        elif opcion == "4":
            eliminar_medico()
        elif opcion == "5":
            listar_medicos()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")

# Funciones internaciones
#Alta interacion
def alta_internacion():
    try:
        print("\n--- ALTA DE INTERNACIÓN ---")
        paciente_id = pedir_numero("ID del paciente: ", "Error: el ID debe ser un número")
        medico_id = pedir_numero("ID del médico: ", "Error: el ID debe ser un número")
        fecha_ingreso = input("Fecha de ingreso (YYYY-MM-DD): ")
        diagnostico = input("Diagnóstico: ")
        habitacion = pedir_numero("Número de habitación: ", "Error: la habitación debe ser un número")
        estado = input("Estado: (Activa/Recuperación): ")
        
        datos = {
            "id": 0,
            "paciente_id": paciente_id,
            "medico_id": medico_id,
            "fecha_ingreso": fecha_ingreso,
            "diagnostico": diagnostico,
            "habitacion": habitacion,
            "estado": estado
        }
        
        respuesta = requests.post(f"{URL_BASE}/internaciones", json=datos, headers=HEADERS)
        
        if respuesta.status_code == 200:
            print("Internación creada exitosamente")
            registrar_log("admin", f"Crear internación: estado {estado}")
        else:
            print("Error: revisa los datos cargados")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#Listar internacioens
def listar_internaciones():
    try:
        print("\n--- LISTADO DE INTERNACIONES ---")
        respuesta = requests.get(f"{URL_BASE}/internaciones")
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            internaciones = datos.get("internaciones", [])
            
            if not internaciones:
                print("No hay internaciones registradas")
            else:
                for i in internaciones:
                    print(f"ID: {i['id']} | Paciente: {i['paciente_id']} | Médico: {i['medico_id']} | Habitación: {i['habitacion']} | Estado: {i['estado']}")
            registrar_log("admin", "Listar internaciones")
        else:
            print(f"Error al obtener internaciones. Código de estado: {respuesta.status_code}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#Buecar internacion
def buscar_internacion():
    try:
        print("\n--- BUSCAR INTERNACIÓN ---")
        id_internacion = pedir_numero("ID de la internación: ", "Error: el ID debe ser un número")
        
        respuesta = requests.get(f"{URL_BASE}/internaciones/{id_internacion}")
        
        if respuesta.status_code == 200:
            i = respuesta.json()["internacion"]
            print(f"\nInternación encontrada:")
            print(f"ID: {i['id']}")
            print(f"Paciente ID: {i['paciente_id']}")
            print(f"Médico ID: {i['medico_id']}")
            print(f"Fecha de ingreso: {i['fecha_ingreso']}")
            print(f"Diagnóstico: {i['diagnostico']}")
            print(f"Habitación: {i['habitacion']}")
            print(f"Estado: {i['estado']}")
            registrar_log("admin", f"Buscar internación: {id_internacion}")
        else:
            print(f"Internación no encontrada. Código de estado: {respuesta.status_code}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#Modficar internacion
def modificar_internacion():
    try:
        print("\n--- MODIFICAR INTERNACIÓN ---")
        id_internacion = pedir_numero("ID de la internación: ", "Error: el ID debe ser un número")
        
        paciente_id = pedir_numero("ID del paciente: ", "Error: el ID debe ser un número")
        medico_id = pedir_numero("ID del médico: ", "Error: el ID debe ser un número")
        fecha_ingreso = input("Fecha de ingreso (YYYY-MM-DD): ")
        diagnostico = input("Diagnóstico: ")
        habitacion = pedir_numero("Número de habitación: ", "Error: la habitación debe ser un número")
        estado = input("Estado: (Activa/Recuperación): ")
        
        datos = {
            "id": id_internacion,
            "paciente_id": paciente_id,
            "medico_id": medico_id,
            "fecha_ingreso": fecha_ingreso,
            "diagnostico": diagnostico,
            "habitacion": habitacion,
            "estado": estado
        }
        
        respuesta = requests.put(f"{URL_BASE}/internaciones/{id_internacion}", json=datos, headers=HEADERS)
        
        if respuesta.status_code == 200:
            print("Internación actualizada exitosamente")
            registrar_log("admin", f"Modificar internación: {id_internacion}")
        else:
            print("Error: revisa los datos cargados", {respuesta.status_code})
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#Eliminar internacion
def eliminar_internacion():
    try:
        print("\n--- ELIMINAR INTERNACIÓN ---")
        id_internacion = pedir_numero("ID de la internación: ", "Error: el ID debe ser un número")
        
        confirmacion = input("¿Estás seguro? (s/n): ")
        if confirmacion.lower() != "s":
            print("Operación cancelada")
            return
        
        respuesta = requests.delete(f"{URL_BASE}/internaciones/{id_internacion}", headers=HEADERS)
        
        if respuesta.status_code == 200:
            print("Internación eliminada exitosamente")
            registrar_log("admin", f"Eliminar internación: {id_internacion}")
        else:
            print("Error al eliminar la internación")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")

#Menu internaciones
def menu_internaciones():
    while True:
        print("\n--- GESTIONAR INTERNACIONES ---")
        print("1 - Alta internación")
        print("2 - Buscar internación")
        print("3 - Modificar internación")
        print("4 - Eliminar internación")
        print("5 - Listar internaciones")
        print("6 - Volver")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            alta_internacion()
        elif opcion == "2":
            buscar_internacion()
        elif opcion == "3":
            modificar_internacion()
        elif opcion == "4":
            eliminar_internacion()
        elif opcion == "5":
            listar_internaciones()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")

#Menu principal
def menu_principal():
    while True:
        print("\n" + "*"*29)
        print("SISTEMA HOSPITALARIO GRUPO 33")
        print("*"*29)
        print("1 - Gestionar pacientes")
        print("2 - Gestionar médicos")
        print("3 - Gestionar internaciones")
        print("4 - Salir")
        print("*"*29)
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            menu_pacientes()
        elif opcion == "2":
            menu_medicos()
        elif opcion == "3":
            menu_internaciones()
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

# Entrada del prog
if __name__ == "__main__":
    menu_principal()