from config import bot
import config
from time import sleep
import re
import logic
import database.db as db

#########################################################
if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
#########################################################

@bot.message_handler(regexp=r"^(crear|crear paquete|cp) ([a-zA-ZÀ-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)*),([+-]?([0-9]*[.])?[0-9]+),([a-zA-Z1-9À-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-Z1-9À-ÖØ-öø-ÿ]+\.?)* (((#|[nN][oO]\.?) ?)?\d{1,4}(( ?[a-zA-Z0-9\-]+)+)?))$")
def crear_paquete(message):
    bot.send_chat_action(message.chat.id, 'typing')
    partes = re.match(r"^(crear|crear paquete|cp) ([a-zA-ZÀ-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)*),([+-]?([0-9]*[.])?[0-9]+),([a-zA-Z1-9À-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-Z1-9À-ÖØ-öø-ÿ]+\.?)* (((#|[nN][oO]\.?) ?)?\d{1,4}(( ?[a-zA-Z0-9\-]+)+)?))$",message.text,flags=re.IGNORECASE)
    #print (partes.groups())
    nombreRemitente = partes[2]
    peso = float(partes[5])
    direccionDestino = partes[7]
    control = logic.crear_paquete (message.from_user.id,nombreRemitente,peso,direccionDestino)
    bot.reply_to(message,f"\U0001F4B0 ¡Paquete Creado!: {nombreRemitente}"
        if control == True 
        else "\U0001F4A9 Tuve problemas registrando la transacción, ejecuta/start y vuelve a intentarlo")


@bot.message_handler(regexp=r"^(listar paquetes|lp)$")
def listar_paquetes(message):
    bot.send_chat_action(message.chat.id, 'typing')
    text = ""
    if logic.verifique_admin(message.from_user.id):
        paquetes = logic.listar_paquetes()
        text = "``` Listado de paquetes:\n\n"
        for paquete in paquetes:
            text += f"| {paquete.id} | ${paquete.nombreRemitente} |\n"
        text += "```"
    else:
        text = f"\U0000274C Esta funcionalidad sólo está disponible para administradores"
    bot.reply_to(message, text, parse_mode="Markdown")


@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,logic.get_welcome_message(bot.get_me()),parse_mode="Markdown")
    bot.send_message(message.chat.id,logic.get_help_message(),parse_mode="Markdown")
    logic.registro_cuenta(message.from_user.id)

@bot.message_handler(commands=['help'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,logic.get_help_message(),parse_mode="Markdown") 

@bot.message_handler(commands=['about'])
def on_command_about(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,logic.get_about_this(config.VERSION), parse_mode="Markdown")


# esto siempre al final del archivo principal es por si no encuentra la opcion
@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    bot.reply_to( message,"\U0001F63F Ups, no entendí lo que me dijiste.")

#########################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################


