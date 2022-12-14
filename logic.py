import database.db as db
from models.Usuario import Usuario
from models.Paquete import Paquete
from models.Estado import Estado
from datetime import datetime
from sqlalchemy import extract, and_
from datetime import datetime

def get_welcome_message(bot_data):
    response = (f"Hola, soy *{bot_data.first_name}* "f"también conocido como *{bot_data.username}*.\n\n""¡Estoy aquí para gestionar el envio de paquetes!")
    return response

def cambiar_estado(paquete_id, user_id, nombreEstado):
    paquete = db.session.query(Paquete).filter(Paquete.id == paquete_id).first()
    db.session.commit()
    if paquete == None:
        return "El paquete no ha sido encontrado."

    estado = Estado(nombreEstado,datetime.now(),user_id)
    db.session.add(estado)
    db.session.commit()
    estado_id = estado.id

    db.session.query(Paquete).filter(Paquete.id == paquete_id).update({'estados_id': estado_id})
    db.session.commit()

    return True

def remover_estado(idEstado):

    paquete = db.session.query(Paquete).filter(Paquete.estados_id == idEstado).first()
    db.session.commit()
    
    if paquete != None:
        print('entro paquete')
        return "El estado esta asociado a un paquete"

    estado = db.session.query(Estado).get(idEstado)
    db.session.delete(estado)
    db.session.commit()

    return True


def registro_cuenta(userInfo):
    usuario = db.session.query(Usuario).get(userInfo.id)
    db.session.commit()
    if usuario == None:
         usuario = Usuario(userInfo.id,"admin","123",userInfo.first_name)
         db.session.add(usuario)
         db.session.commit()
         return True
    return False

def verifique_admin(user_id):
    administrador = [1898458696, 5141666038, 1923311798]
    if user_id in administrador:
        return True
    else:
        return False

def listar_paquetes_admin():
    text = ""
    #paquetes que aún no han sido entregados
    paquetes = db.session.query(Paquete).all()
    if paquetes == []:
        return "No hay paquetes registrados"
    text = "``` Listado de paquetes:\n\n"
    for paquete in paquetes:
        text += f" {paquete.id} | {paquete.nombreRemitente} | {paquete.direccionDestino} | {paquete.estados_id}\n"
    text += "```"
    return text

def listar_paquetes_por_usuario(id_usuario):
    #paquetes registrados que le pertenecen al usuario
    # id_usuario = 1898458696
    text = ""
    stmt = db.session.query(Paquete.id, Paquete.nombreRemitente, Paquete.direccionDestino, Paquete.estados_id, Paquete.peso,Paquete.fechaActual).where(Paquete.estados.has(Estado.usuarios_id == id_usuario))
    paquetes = db.session.execute(stmt).all() 
    if paquetes == []:
        return "No se encontraron paquetes para este usuario"
    text = "``` Listado de paquetes:\n\n"
    for paquete in paquetes:
        text += f" {paquete.id} | {paquete.nombreRemitente} | {paquete.direccionDestino} | {paquete.estados_id}\n"
    text += "```"
    return text

def crear_paquete (user_id, nombreRemitente,peso,direccionDestino):
    if peso <= 0:
        return False 
    estado = Estado("pendiente de recepción",datetime.now(),user_id)
    db.session.add(estado)
    db.session.commit()
    estado_id=estado
    paquete = Paquete(repr(estado_id),user_id,datetime.now(),nombreRemitente,peso,direccionDestino)
    db.session.add(paquete)
    db.session.commit()
    return True

def actualizar_paquete (user_id,  nombreRemitente,peso,direccionDestino):
    paquete = db.session.query(Paquete).get(user_id)
    db.session.commit()
    if not paquete:
        return False
    db.session.commit()
    return True

def permite_eliminar(id_usuario, id_paquete):
    stmt = db.session.query(Paquete.id, Paquete.estados_id).where(Paquete.id == id_paquete)
    paquetes = db.session.execute(stmt).all() 
    for paquete in paquetes:
        stmt = db.session.query(Estado.id, Estado.tipo, Estado.usuarios_id).where(Estado.id == paquete.estados_id)
        estados = db.session.execute(stmt).all() 
        # print(f"Estados Encontrados:", estados, id_usuario)
        for estado in estados:
            if (estado.tipo == "pendiente de recepción" and estado.usuarios_id != str(id_usuario)):
                return False
            elif estado.tipo == "recogido":
                return False
    # print(paquetes)
    return True

def eliminar_paquete_by_id(id_paquete):
    paquete = db.session.query(Paquete).get(id_paquete)
    # print(f"Paquete Encontrado:",id_paquete, paquete)
    if paquete != None:
        #  usuario = Usuario(userInfo.id,"admin","123",userInfo.first_name)
        db.session.delete(paquete)
        db.session.commit()
        return (f"Paquete {paquete.id} eliminado")
    return "Paquete no encontrado"
    
def consultar_estados_by_id(id_usuario, id_paquete):
    # id_usuario = 1898458696
    text = ""
    stmt = db.session.query(Paquete.id, Paquete.estados_id).where(Paquete.id == id_paquete)
    paquetes = db.session.execute(stmt).all() 
    for paquete in paquetes:
        stmt = db.session.query(Estado.id, Estado.tipo, Estado.usuarios_id, Estado.fechaHora).where(Estado.id == paquete.estados_id)
        estados = db.session.execute(stmt).all() 
        if estados == []:
            return "No se encontraron estados para este paquete"
        text = "``` Listado de estados:\n\n"
        for estado in estados:
            text += f" {estado.id} | {estado.tipo} | {estado.fechaHora}\n"
        text += "```"        
    return text

def paquete_perteneceUsuario(id_paquete, id_usuario):
    stmt = db.session.query(Paquete.id, Paquete.estados_id).where(Paquete.id == id_paquete)
    paquetes = db.session.execute(stmt).all() 
    for paquete in paquetes:
        stmt = db.session.query(Estado.id, Estado.tipo, Estado.usuarios_id).where(Estado.id == paquete.estados_id)
        estados = db.session.execute(stmt).all() 
        for estado in estados:
            if (estado.usuarios_id == str(id_usuario)):
                return True
    return False

def get_help_message (idUsuario):
    if verifique_admin(idUsuario):
        return (
            "Estos son los comandos y órdenes disponibles:\n"
            "\n"
            "*/start* - Inicia la interacción con el bot (obligatorio)\n"
            "*/help* - Muestra este mensaje de ayuda\n"
            "*/about* - Muestra detalles de esta aplicación\n"
            f"*Admin* \n"
            "*listar paquetes|lp* - Lista los paquetes exitentes para el administrador\n"
            "*cambiar estado|camb estd|cae* - cambiar el estado de un paquete\n"
            "*eliminar estado|elim estd|ee* - Eliminar estado de un paquete\n"
            )
    else:
        return (
            "Estos son los comandos y órdenes disponibles:\n"
            "\n"
            "*/start* - Inicia la interacción con el bot (obligatorio)\n"
            "*/help* - Muestra este mensaje de ayuda\n"
            "*/about* - Muestra detalles de esta aplicación\n"
            "*crear|crear paquete|cp {nombre remitente,peso,direccion destino}* - Registra un paquete\n"
            "*listar paquetes|lp* - Lista los paquetes exitentes para el usuario\n"
            "*eliminar paquetes|e {id_paquete}* - Elimina un paquete\n"
            "*consultar estados|ce {id_paquete}* - Consulta estados de un paquete\n"
        )

def get_about_this(VERSION):
    response = (f"Gestion de envio de paquetes BOT (pyTelegramBot) v{VERSION}"
    "\n\n"
    "Desarrollado por"
    "\n" 
    "Angie Daniela Chisco Cadavid <chiscoangiedaniela@gmail.com>"
    "\n"
    "Brian Camilo Piragauta Mesa <brianpiragauta@gmail.com>"
    "\n"
    "Juan Pablo Toro Arias <juanp.toroa@autonoma.edu.co>"
    )
    return response


