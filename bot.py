from config import bot
import config
from time import sleep
import re
import logic
import database.db as db
from telebot import types

#########################################################
id_paquete_eliminar = None
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
    if logic.verifique_admin(message.from_user.id) == "True":
        text= logic.listar_paquetes_admin();
    else:
        text = logic.listar_paquetes_por_usuario(message.from_user.id);
    bot.reply_to(message, text, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,logic.get_welcome_message(bot.get_me()),parse_mode="Markdown")
    bot.send_message(message.chat.id,logic.get_help_message(message.from_user.id),parse_mode="Markdown")
    logic.registro_cuenta(message.from_user)
    # if logic.verifique_admin(message.from_user.id):
    #     bot.send_message(message.chat.id,"Ingrese su contraseña",parse_mode="Markdown")

@bot.message_handler(regexp=r"^(eliminar paquete|e) \d+$")
def eliminar_paquete_by_id(message):
    bot.send_chat_action(message.chat.id, 'typing')    
    partes = re.split("^(eliminar paquete|e)",message.text)
    #Consultar si el paquete tiene el estado recogido.
    global id_paquete_eliminar 
    id_paquete_eliminar = partes[2].strip()
    if logic.permite_eliminar(message.from_user.id, id_paquete_eliminar):
        try:
            #Mensaje validacion
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('SI', 'NO')
            response = bot.reply_to(message, '¿Confirma eliminar este paquete?', reply_markup=markup)
            bot.register_next_step_handler(response, eliminar_paquete)
        except Exception as e:
            bot.reply_to(message, f"Algo terrible sucedió: {e}")
            id_paquete_eliminar = None

    else:
        bot.reply_to(message, "No se puede eliminar este paquete, valide que le pertenezca y que no tenga estado 'recogido'", parse_mode="Markdown")

def eliminar_paquete(message):
    global id_paquete_eliminar
    res = message.text
    if res =="SI":
        bot.reply_to(message, logic.eliminar_paquete_by_id(id_paquete_eliminar), parse_mode="Markdown")
    else:
        bot.reply_to(message, "No se ha eliminado el paquete", parse_mode="Markdown")
        id_paquete_eliminar = None
    
@bot.message_handler(regexp=r"^(consultar estados|ce) \d+$")
def consultar_estados(message):
    bot.send_chat_action(message.chat.id, 'typing')    
    partes = re.split("^(consultar estados|ce)",message.text)
    if logic.paquete_perteneceUsuario(partes[2].strip(), message.from_user.id) == False:
        bot.reply_to(message, "El paquete no pertenece a este usuario", parse_mode="Markdown")
    else:
        bot.reply_to(message, logic.consultar_estados_by_id(message.from_user.id,partes[2].strip()), parse_mode="Markdown")

@bot.message_handler(commands=['help'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id,logic.get_help_message(message.from_user.id),parse_mode="Markdown") 

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


@bot.message_handler(regexp=r"^(cambiar estado|camb estd|cae) ([a-zA-ZÀ-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)*),([+-]?([0-9]*[.])?[0-9]+),([a-zA-Z1-9À-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-Z1-9À-ÖØ-öø-ÿ]+\.?)* (((#|[nN][oO]\.?) ?)?\d{1,4}(( ?[a-zA-Z0-9\-]+)+)?))$")
def cambiar_estado(message):
    bot.send_chat_action(message.chat.id, 'typing')
    partes = re.match(r"^(cambiar estado) ([a-zA-ZÀ-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-ZÀ-ÖØ-öø-ÿ]+\.?)*),([+-]?([0-9]*[.])?[0-9]+),([a-zA-Z1-9À-ÖØ-öø-ÿ]+\.?(( |\-)[a-zA-Z1-9À-ÖØ-öø-ÿ]+\.?)* (((#|[nN][oO]\.?) ?)?\d{1,4}(( ?[a-zA-Z0-9\-]+)+)?))$",message.text,flags=re.IGNORECASE)
    #print (partes.groups())
    nombreRemitente = partes[2]
    peso = float(partes[5])
    direccionDestino = partes[7]
    control = logic.crear_paquete (message.from_user.id,nombreRemitente,peso,direccionDestino)
    bot.reply_to(message,f"\U0001F4B0 ¡Paquete Creado!: {nombreRemitente}"
        if control == True 
        else "\U0001F4A9 Tuve problemas registrando la transacción, ejecuta/start y vuelve a intentarlo")
#########################################################
if __name__ == '__main__':
    bot.polling(timeout=20)
#########################################################


