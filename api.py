from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import json, secrets
import os

#Creamos nuestra aplicació
app = FastAPI()

#Configuramos la seguridad con bearer token
secutity = HTTPBearer()

#Token
if os.path.exists("token.txt"):
    with open("token.txt", "r") as f:
        TOKEN_VALIDO = f.read().strip()
else:
    TOKEN_VALIDO = secrets.token_hex(32)
    with open("token.txt", "w") as f:
        f.write(TOKEN_VALIDO)

print(f"Token actual: {TOKEN_VALIDO}")

#Modelos pydantic

#PAciente
class Paciente(BaseModel):
    id: int
    dni: str
    nombre: str
    apellido: str
    edad: int
    telefono: str
    obra_social: str

#Médico
class Medico(BaseModel):
    id: int
    matricula: str
    nombre: str
    apellido: str
    especialidad: str
    telefono: str

#Internación
class Internacion(BaseModel):
    id: int
    paciente_id: int
    medico_id: int
    fecha_ingreso: str
    diagnostico: str
    habitacion: int
    estado: str

#Funciones JSON

def cargar_pacientes():
    if os.path.exists("pacientes.json"):
        with open("pacientes.json", "r") as f:
            return json.load(f)
    return []

def guardar_pacientes(pacientes):
    with open("pacientes.json", "w") as f:
        json.dump(pacientes, f, indent=4)

def cargar_medicos():
    if os.path.exists("medicos.json"):
        with open("medicos.json", "r") as f:
            return json.load(f)
    return []

def guardar_medicos(medicos):
    with open("medicos.json", "w") as f:
        json.dump(medicos, f, indent=4)

def cargar_internaciones():
    if os.path.exists("internaciones.json"):
        with open("internaciones.json", "r") as f:
            return json.load(f)
    return []

def guardar_internaciones(internaciones):
    with open("internaciones.json", "w") as f:
        json.dump(internaciones, f, indent=4)

# Obtener ids
def obtener_proximo_id_paciente():
    """Calcula el próximo ID para paciente"""
    pacientes = cargar_pacientes()
    if not pacientes:
        return 1
    
    max_id = 0
    for p in pacientes:
        if p["id"] > max_id:
            max_id = p["id"]
    
    return max_id + 1

def obtener_proximo_id_medico():
    """Calcula el próximo ID para médico"""
    medicos = cargar_medicos()
    if not medicos:
        return 1
    
    max_id = 0
    for m in medicos:
        if m["id"] > max_id:
            max_id = m["id"]
    
    return max_id + 1

def obtener_proximo_id_internacion():
    """Calcula el próximo ID para internación"""
    internaciones = cargar_internaciones()
    if not internaciones:
        return 1
    
    max_id = 0
    for i in internaciones:
        if i["id"] > max_id:
            max_id = i["id"]
    
    return max_id + 1        

def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(secutity)):
    token = credentials.credentials
    if token != TOKEN_VALIDO:
        raise HTTPException(status_code=401, detail="Token inválido")
    return token

#Endpoint de pruebita
@app.get("/")
def raiz():
    return {"mensaje": "Bienvenido a la API del hospital"}

#Endpoints pacientes
#POST paciente
@app.post("/pacientes")
def crear_paciente(paciente: Paciente, token: str = Depends(verificar_token)):
    pacientes = cargar_pacientes()

    if not paciente.nombre or not paciente.apellido:
        raise HTTPException(status_code=400, detail="El nombre y apellido son obligatorios")
    
    if paciente.edad <= 0:
        raise HTTPException(status_code=400, detail="La edad debe ser mayor a 0")
    
    paciente_dict = paciente.model_dump()
    paciente_dict["id"] = obtener_proximo_id_paciente()
    pacientes.append(paciente_dict)
    guardar_pacientes(pacientes)
    return {"mensaje": "Paciente creado exitosamente", "paciente": paciente_dict}

#GET pacientes
@app.get("/pacientes")
def listar_pacientes():
    pacientes = cargar_pacientes()
    return {"pacientes": pacientes}

#GET paciente especifico
@app.get("/pacientes/{id}")
def obtener_paciente (id: int):
    pacientes = cargar_pacientes()

    for paciente in pacientes:
        if paciente["id"] == id:
            return {"paciente": paciente}
    raise HTTPException(status_code=404, detail="Paciente no encontrado")

#PUT paciente especifico
@app.put("/pacientes/{id}")
def modificar_paciente(id: int, paciente_actualizado: Paciente, token: str = Depends(verificar_token)):
    pacientes = cargar_pacientes()

    if not paciente_actualizado.nombre or not paciente_actualizado.apellido:
        raise HTTPException(status_code=400, detail="El nombre y apellido son obligatorios")
    
    if paciente_actualizado.edad <= 0:
        raise HTTPException(status_code=400, detail="La edad debe ser mayor a 0")

    for i, paciente in enumerate(pacientes):
        if paciente["id"] == id:
            pacientes[i] = paciente_actualizado.model_dump()
            guardar_pacientes(pacientes)
            return {"mensaje": "Paciente modificado exitosamente", "paciente": pacientes[i]}
    
    raise HTTPException(status_code=404, detail="Paciente no encontrado")

#DELETE paciente especifico
@app.delete("/pacientes/{id}")
def eliminar_paciente(id: int, token: str = Depends(verificar_token)):
    pacientes = cargar_pacientes()

    for i, paciente in enumerate(pacientes):
        if paciente["id"] == id:
            paciente_eliminado = pacientes.pop(i)
            guardar_pacientes(pacientes)
            return {"mensaje": "Paciente eliminado exitosamente", "paciente": paciente_eliminado}
    
    raise HTTPException(status_code=404, detail="Paciente no encontrado")

#Endpoints médicos
#POST médico

@app.post("/medicos")
def crear_medico(medico: Medico, token: str = Depends(verificar_token)):
    medicos = cargar_medicos()
    
    if not medico.matricula or not medico.especialidad:
        raise HTTPException(status_code=400, detail="LA matrícula y la especialidad son obligatorias")
    
    medico_dict = medico.model_dump()
    medico_dict["id"] = obtener_proximo_id_medico()
    medicos.append(medico_dict)
    guardar_medicos(medicos)

    return {"mensaje": "Médico creado exitosamente", "medico": medico_dict}

#GET médicos
@app.get("/medicos")
def listar_medicos():
    medicos = cargar_medicos()
    return {"medicos": medicos}

#GET médico específico
@app.get("/medicos/{id}")
def obtener_medico(id: int):
    medicos = cargar_medicos()

    for medico in medicos:
        if medico["id"] == id:
            return {"medico": medico}
    raise HTTPException(status_code=404, detail="Médico no encontrado")

#PUT médico específico
@app.put("/medicos/{id}")
def modificar_medico(id: int, medico_actualizado: Medico, token: str = Depends(verificar_token)):
    medicos = cargar_medicos()
    
    if not medico_actualizado.matricula or not medico_actualizado.especialidad:
        raise HTTPException(status_code=400, detail="Matrícula y especialidad son obligatorias")
    
    for i, medico in enumerate(medicos):
        if medico["id"] == id:
            medicos[i] = medico_actualizado.model_dump()
            guardar_medicos(medicos)
            return {"mensaje": "Médico actualizado exitosamente", "medico": medicos[i]}
    
    raise HTTPException(status_code=404, detail="Médico no encontrado")

@app.delete("/medicos/{id}")
def eliminar_medico(id: int, token: str = Depends(verificar_token)):
    medicos = cargar_medicos()
    
    for i, medico in enumerate(medicos):
        if medico["id"] == id:
            medico_eliminado = medicos.pop(i)
            guardar_medicos(medicos)
            return {"mensaje": "Médico eliminado exitosamente", "medico": medico_eliminado}
    
    raise HTTPException(status_code=404, detail="Médico no encontrado")

#Endpoints internaciones
#POST internación
@app.post("/internaciones")
def crear_internacion(internacion: Internacion, token: str = Depends(verificar_token)):
    internaciones = cargar_internaciones()
    pacientes = cargar_pacientes()
    medicos = cargar_medicos()
    
    paciente_existe = False
    for p in pacientes:
        if p["id"] == internacion.paciente_id:
            paciente_existe = True
            break
    if not paciente_existe:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    
    medico_existe = False
    for m in medicos:
        if m["id"] == internacion.medico_id:
            medico_existe = True
            break
    if not medico_existe:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    if internacion.habitacion <= 0:
        raise HTTPException(status_code=400, detail="Habitación debe ser un número positivo")
    
    internacion_dict = internacion.model_dump()
    internacion_dict["id"] = obtener_proximo_id_internacion()
    internaciones.append(internacion_dict)
    guardar_internaciones(internaciones)
    
    return {"mensaje": "Internación creada exitosamente", "internacion": internacion_dict}

#GET internaciones
@app.get("/internaciones")
def listar_internaciones():
    internaciones = cargar_internaciones()
    return {"internaciones": internaciones}

#GET internación específica
@app.get("/internaciones/{id}")
def obtener_internacion(id: int):
    internaciones = cargar_internaciones()
    
    for internacion in internaciones:
        if internacion["id"] == id:
            return {"internacion": internacion}
    
    raise HTTPException(status_code=404, detail="Internación no encontrada")

#PUT internación específica
@app.put("/internaciones/{id}")
def modificar_internacion(id: int, internacion_actualizada: Internacion, token: str = Depends(verificar_token)):
    internaciones = cargar_internaciones()
    pacientes = cargar_pacientes()
    medicos = cargar_medicos()
    
    paciente_existe = False
    for p in pacientes:
        if p["id"] == internacion.paciente_id:
            paciente_existe = True
            break
    if not paciente_existe:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    
    medico_existe = False
    for m in medicos:
        if m["id"] == internacion.medico_id:
            medico_existe = True
            break
    if not medico_existe:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    if internacion_actualizada.habitacion <= 0:
        raise HTTPException(status_code=400, detail="Habitación debe ser un número positivo")
    
    for i, internacion in enumerate(internaciones):
        if internacion["id"] == id:
            internaciones[i] = internacion_actualizada.model_dump()
            guardar_internaciones(internaciones)
            return {"mensaje": "Internación actualizada exitosamente", "internacion": internaciones[i]}
    
    raise HTTPException(status_code=404, detail="Internación no encontrada")

#DELETE internación específica
@app.delete("/internaciones/{id}")
def eliminar_internacion(id: int, token: str = Depends(verificar_token)):
    internaciones = cargar_internaciones()
    
    for i, internacion in enumerate(internaciones):
        if internacion["id"] == id:
            internacion_eliminada = internaciones.pop(i)
            guardar_internaciones(internaciones)
            return {"mensaje": "Internación eliminada exitosamente", "internacion": internacion_eliminada}
    
    raise HTTPException(status_code=404, detail="Internación no encontrada")