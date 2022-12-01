import database.db as db
from models.Usuario import Usuario
from models.Paquete import Paquete
from models.Estado import Estado
from datetime import datetime
from sqlalchemy import extract

def get_welcome_message(bot_data):
    response = (f"Hola, soy *{bot_data.first_name}* "f"también conocido como *{bot_data.username}*.\n\n""¡Estoy aquí para gestionar el envio de paquetes!")
    return response

def registro_cuenta(user_id):
    usuario = db.session.query(Usuario).get(user_id)
    db.session.commit()
    if usuario == None:
        usuario = Usuario(user_id,"admin","123","DANI")
        db.session.add(usuario)
        db.session.commit()
        return True
    return False

def verifique_admin(user_id):
    administrador = [1898458696]
    return user_id in administrador

def listar_paquetes():
    paquetes = db.session.query(Paquete).all()
    return paquetes

def crear_paquete (user_id, nombreRemitente,peso,direccionDestino):
    if peso <= 0:
        return False 
    estado = Estado("en procesos",datetime.now(),user_id)
    db.session.add(estado)
    paquete = Paquete("1",user_id,datetime.now(),nombreRemitente,peso,direccionDestino)
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


def get_help_message ():
    response = (
        "Estos son los comandos y órdenes disponibles:\n"
        "\n"
        "*/start* - Inicia la interacción con el bot (obligatorio)\n"
        "*/help* - Muestra este mensaje de ayuda\n"
        "*/about* - Muestra detalles de esta aplicación\n"
        "*usuario {rol}* - Muestra opciones del usuarios eleccionado\n"
        #"*gane|gané|g {cantidad}* - Registra un saldo positivo\n"
        #"*gaste|gasté|gg {cantidad}* - Registra un saldo negativo\n"
        #"*listar ganancias|lg en {índice_mes} de {año}* - Lista las ganancias de un mes/año\n"
        #"*listar gastos|lgg en {mes} de {año}* - Lista los gastos de un mes/año\n"
        #"*obtener saldo|s* - Muestra el saldo actual (disponible)\n"
        #"*remover|r ganancia|g|gasto|gg {índice}* - Remueve una ganancia o un gasto según su índice\n"
        #"*listar cuentas|lc* - Lista las cuentas registradas (sólo admin)\n"
        )
    return response

def get_about_this(VERSION):
    response = (f"Gestion de envio de paquetes BOT (pyTelegramBot) v{VERSION}"
    "\n\n"
    "Desarrollado por"
    "\n" 
    "Angie Daniela Chisco Cadavid <chiscoangiedaniela@gmail.com>"
    "\n"
    "Brian Camilo Piragauta Mesa <brianpiragauta@gmail.com>"
    "\n"
    "juan Pablo Toro Arias <juanp.toroa@autonoma.edu.co>"
    )
    return response


