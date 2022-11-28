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
        usuario = Usuario(user_id, 0)
        db.session.add(Usuario)
        db.session.commit()
        return True
    return False

def get_help_message ():
    response = (
        "Estos son los comandos y órdenes disponibles:\n"
        "\n"
        "*/start* - Inicia la interacción con el bot (obligatorio)\n"
        "*/help* - Muestra este mensaje de ayuda\n"
        "*/about* - Muestra detalles de esta aplicación\n"
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
    response = (f"Simple Expenses Bot (pyTelegramBot) v{VERSION}"
    "\n\n"
    "Desarrollado por Angie Daniela Chisco Cadavid <chiscoangiedaniela@gmail.com>"
    "Brian Camilo Piragauta Mesa <brianpiragauta@gmail.com>"
    "juan Pablo Toro Arias <juanp.toroa@autonoma.edu.co>"
    )
    return response


