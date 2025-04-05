import logging
import random
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configuración del bot
TOKEN = "6278513639:AAHnMq7dI0uxt-ZCnsHFHjLHbb4WVoEuROw"

# Tiempo mínimo entre usos del comando (en segundos)
TIEMPO_MINIMO = 30
USOS_MAXIMOS = 500000

# Configuración del logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Leer registros al iniciar
with open("ssn.txt", "r", encoding="utf-8") as f:
    REGISTROS = [line.strip() for line in f if line.strip()]

# Diccionario para guardar qué usuarios ya vieron qué registros
usos_usuario = {}
tiempo_ultimo_uso = {}

# Manejador del comando /ssn
async def ssn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    now = datetime.now()

    # Verificar espera de tiempo
    if user_id in tiempo_ultimo_uso:
        diferencia = (now - tiempo_ultimo_uso[user_id]).total_seconds()
        if diferencia < TIEMPO_MINIMO:
            await update.message.reply_text(f"⏳ Espera {int(TIEMPO_MINIMO - diferencia)} segundos antes de volver a usar este comando.")
            return

    # Obtener registros vistos
    vistos = usos_usuario.get(user_id, [])

    # Verificar si quedan registros por mostrar
    disponibles = [r for r in REGISTROS if r not in vistos]
    if not disponibles:
        await update.message.reply_text("✅ Ya viste todos los registros disponibles.")
        return

    # Elegir uno nuevo al azar
    elegido = random.choice(disponibles)
    vistos.append(elegido)
    usos_usuario[user_id] = vistos
    tiempo_ultimo_uso[user_id] = now

    await update.message.reply_text(f"📄 {elegido}")

# Manejador del comando /help
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Usa /ssn para obtener un registro. Espera 30 segundos entre usos.")

# Función principal
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("ssn", ssn))
    app.add_handler(CommandHandler("help", help))

    app.run_polling()

if __name__ == '__main__':
    main()
