import logging
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

TIEMPO_MINIMO = 30  # segundos

# Leer y dividir los registros del archivo
def cargar_registros():
    try:
        with open("9K SSN BY @Mr_vision0.txt", "r", encoding="utf-16") as f:
            texto = f.read()
    except UnicodeError:
        with open("9K SSN BY @Mr_vision0.txt", "r", encoding="latin-1") as f:
            texto = f.read()

    # Dividir por bloques usando líneas separadoras
    registros_raw = texto.strip().split('--------------------------')
    registros = []

    for bloque in registros_raw:
        name = re.search(r'Name:\s*(.+)', bloque)
        dob = re.search(r'DOB:\s*(.+)', bloque)
        address = re.search(r'Address:\s*(.+)', bloque)

        if name and dob and address:
            registros.append({
                'name': name.group(1).strip(),
                'dob': dob.group(1).strip(),
                'address': address.group(1).strip()
            })

    return registros

REGISTROS = cargar_registros()

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
        await update.message.reply_text(f"⏳ Espera {restante} segundos antes de volver a usar el comando.")
        return

    if data['indice'] >= len(REGISTROS):
        await update.message.reply_text("✅ Ya viste todos los registros disponibles.")
        return

    registro = REGISTROS[data['indice']]
    mensaje = (
        f"🧾 *SSN Registrado:*\n\n"
        f"👤 *Nombre:* {registro['name']}\n"
        f"📅 *Fecha de nacimiento:* {registro['dob']}\n"
        f"🏠 *Dirección:* {registro['address']}"
    )

    await update.message.reply_text(mensaje, parse_mode="Markdown")
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
