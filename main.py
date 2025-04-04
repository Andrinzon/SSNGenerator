import logging
import random
import re
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configuración del bot
TOKEN = "6278513639:AAHnMq7dI0uxt-ZCnsHFHjLHbb4WVoEuROw"

# Logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Tiempo mínimo entre comandos y máximo de registros
TIEMPO_MINIMO = 30  # segundos

# Carga del archivo (detectamos codificación automática entre utf-16 y latin1)
try:
    with open("9K SSN BY @Mr_vision0.txt", "r", encoding="utf-16") as f:
        BLOQUES = [line.strip() for line in f if line.strip()]
except UnicodeError:
    with open("9K SSN BY @Mr_vision0.txt", "r", encoding="latin-1") as f:
        BLOQUES = [line.strip() for line in f if line.strip()]

# Comando /ssn
async def ssn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.now()

    if 'usuarios' not in context.chat_data:
        context.chat_data['usuarios'] = {}

    usuarios = context.chat_data['usuarios']

    if user_id not in usuarios:
        usuarios[user_id] = {'indice': 0, 'ultimo_uso': now - timedelta(seconds=TIEMPO_MINIMO + 1)}

    data = usuarios[user_id]

    if (now - data['ultimo_uso']).total_seconds() < TIEMPO_MINIMO:
        restante = int(TIEMPO_MINIMO - (now - data['ultimo_uso']).total_seconds())
        await update.message.reply_text(f"⏳ Espera {restante} segundos antes de usar el comando nuevamente.")
        return

    if data['indice'] >= len(BLOQUES):
        await update.message.reply_text("✅ Ya viste todos los registros disponibles.")
        return

    mensaje = BLOQUES[data['indice']]
    await update.message.reply_text(f"📄 Registro #{data['indice']+1}:\n\n{mensaje}")
    data['indice'] += 1
    data['ultimo_uso'] = now

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Usa /ssn para recibir un registro. Puedes volver a usarlo cada 30 segundos.")

# Main
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("ssn", ssn))
    app.add_handler(CommandHandler("help", help_command))
    app.run_polling()

if __name__ == '__main__':
    main()
