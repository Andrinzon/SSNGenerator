import logging
from datetime import datetime, timedelta
from telegram.ext import CommandHandler, Updater

# Configuración del bot
TOKEN = "6278513639:AAHnMq7dI0uxt-ZCnsHFHjLHbb4WVoEuROw"

# Configuración del logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Tiempo mínimo entre usos del comando (en segundos)
TIEMPO_MINIMO = 30

# Cargar el contenido del archivo al iniciar el bot
with open('9K SSN BY @Mr_vision0.txt', 'r', encoding='latin-1') as f:
    BLOQUES = [line.strip() for line in f if line.strip()]

# Manejador del comando /ssn
def ssn(update, context):
    user_id = update.effective_user.id
    now = datetime.now()

    if 'usuarios' not in context.chat_data:
        context.chat_data['usuarios'] = {}

    usuarios = context.chat_data['usuarios']

    # Inicializar el usuario si no está registrado
    if user_id not in usuarios:
        usuarios[user_id] = {
            'indice': 0,
            'ultimo_uso': now - timedelta(seconds=TIEMPO_MINIMO + 1)
        }

    datos = usuarios[user_id]

    # Control de tiempo
    if (now - datos['ultimo_uso']).total_seconds() < TIEMPO_MINIMO:
        espera = int(TIEMPO_MINIMO - (now - datos['ultimo_uso']).total_seconds())
        update.message.reply_text(f"⏳ Debes esperar {espera} segundos antes de volver a usar el comando.")
        return

    # Validar si ya no hay más registros
    if datos['indice'] >= len(BLOQUES):
        update.message.reply_text("✅ Ya viste todos los registros disponibles.")
        return

    # Obtener el texto correspondiente
    texto = BLOQUES[datos['indice']]
    datos['indice'] += 1
    datos['ultimo_uso'] = now

    # Dividir y formatear
    partes = [p.strip() for p in texto.split('|')]
    mensaje = "📄 Información del SSN:\n\n"

    for parte in partes:
        if "Name" in parte:
            mensaje += f"👤 {parte}\n"
        elif "SSN" in parte:
            mensaje += f"🔢 {parte}\n"
        elif "DOB" in parte or "Date" in parte:
            mensaje += f"🎂 {parte}\n"
        elif "State" in parte or "Location" in parte:
            mensaje += f"📍 {parte}\n"
        else:
            mensaje += f"📌 {parte}\n"

    update.message.reply_text(mensaje)
    context.chat_data['usuarios'] = usuarios

# Manejador del comando /help
def help(update, context):
    update.message.reply_text("ℹ️ Usa /ssn para recibir un dato ordenado.\nDebes esperar 30 segundos entre usos.")

# Función principal
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('ssn', ssn))
    dp.add_handler(CommandHandler('help', help))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
