import database.db as db
from models.Usuario import Usuario
from models.Paquete import Paquete
from models.Estado import Estado
from datetime import datetime
from sqlalchemy import extract

def get_welcome_message(bot_data):
    response = (f"Hola, soy *{bot_data.first_name}* "f"también conocido como *{bot_data.username}*.\n\n""¡Estoy aquí para gestionar el envio de paquetes!")
    return response

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
    administrador = [1898458696, 5141666038]
    if user_id in administrador:
        return True
    else:
        return False

def listar_paquetes_admin():
    text = ""
    #paquetes que aún no han sido entregados
    paquetes = db.session.query(Paquete).all()
    text = "``` Listado de paquetes:\n\n"
    for paquete in paquetes:
        text += f"| {paquete.id} | ${paquete.nombreRemitente} |\n"
        text += "```"
    return text

def listar_paquetes_por_usuario(id_usuario):
    #paquetes registrados que le pertenecen al usuario
    # id_usuario = 1898458696
    text = ""
    stmt = db.session.query(Paquete.id, Paquete.nombreRemitente, Paquete.direccionDestino, Paquete.estados_id, Paquete.peso,Paquete.fechaActual).where(Paquete.estados.has(Estado.usuarios_id == id_usuario), Paquete.estados.has(Estado.tipo == "en procesos"))
    paquetes = db.session.execute(stmt).all() 
    if paquetes == []:
        return "No se encontraron paquetes para este usuario"
    text = "``` Listado de paquetes:\n\n"
    for paquete in paquetes:
        text += f" {paquete.id} | {paquete.nombreRemitente} | {paquete.direccionDestino} | {paquete.estados_id}\n"
    text += "```"
    return text

def crear_paquete (user_id, nombreRemitente,peso,direccionDestino):
    resultado=0
    if peso <= 0:
        return False 
    estado = Estado("en procesos",datetime.now(),user_id)
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
    stmt = db.session.query(Paquete.id, Paquete.estados_id).where(Paquete.id == id_paquete, Paquete.estados.has(Estado.usuarios_id == id_usuario), Paquete.estados.has(Estado.tipo == "recogido"))
    paquetes = db.session.execute(stmt).all() 
    if paquetes == []:
        return True
    else:
        return False

def eliminar_paquete_by_id(id_paquete):
    paquete = db.session.query(Paquete).get(id_paquete)
    print(f"Paquete Encontrado:", paquete)
    if paquete != None:
        #  usuario = Usuario(userInfo.id,"admin","123",userInfo.first_name)
        db.session.delete(paquete)
        db.session.commit()
        return (f"Paquete {paquete.id} eliminado")
    return "Paquete no encontrado"
    
def consultar_estados_by_id(id_usuario, id_paquete):
    # id_usuario = 1898458696
    text = ""
    stmt = db.session.query(Paquete.id, Paquete.nombreRemitente, Paquete.direccionDestino, Paquete.estados_id, Paquete.peso,Paquete.fechaActual).where(Paquete.estados.has(Estado.usuarios_id == id_usuario), Paquete.estados.has(Estado.tipo == "en procesos"))
    paquetes = db.session.execute(stmt).all() 
    if paquetes == []:
        return "No se encontraron paquetes para este usuario"
    text = "``` Listado de paquetes:\n\n"
    for paquete in paquetes:
        text += f" {paquete.id} | {paquete.nombreRemitente} | {paquete.direccionDestino} | {paquete.estados_id}\n"
    text += "```"
    return text

def get_help_message (idUsuario):
    if verifique_admin(idUsuario) == "True":
        return (
            "Estos son los comandos y órdenes disponibles:\n"
            "\n"
            "*/start* - Inicia la interacción con el bot (obligatorio)\n"
            "*/help* - Muestra este mensaje de ayuda\n"
            "*/about* - Muestra detalles de esta aplicación\n"
            f"*Admin* \n"
            "*listar paquetes|lp* - Lista los paquetes exitentes para el administrador\n"
            "*agregar estado|ae* - Agregar un nuevo estado a un paquete\n"
            "*eliminar estado|ee* - Eliminar estado de un paquete, cuando hay error\n"
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


