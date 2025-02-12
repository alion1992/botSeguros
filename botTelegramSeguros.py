from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext


TOKEN = "7676914682:AAGseR0GPhPwJZSOYC5uvGbKsFlxlEvLMco"
CATEGORIAS = {
    "Vehículos": ["Moto", "Coche", "Triciclo"],
    "Moto": [">50cc", "<50cc"],
    "Coche": ["<120cc>", "entre 121 cv y 200 cv", "> 201 cv"],
    ">50cc": ["Permiso A1", "Permiso A2"],
    "<50cc": [">18 años"],
    "> 201 cv": ["Emision 30g", "Emision 50g"],

}
historico = []

async def start(update: Update, context: CallbackContext) -> None:
    """Muestra un mensaje de bienvenida."""
    await update.message.reply_text(f"¡Hola, {update.effective_user.first_name}! 😊\nUsa /menu para ver opciones.")

async def menu(update: Update, context: CallbackContext) -> None:
    historico = []
    keyboard = [[option] for option in CATEGORIAS["Vehículos"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Elige una categoría:", reply_markup=reply_markup)

async def option_selected(update: Update, context: CallbackContext) -> None:

    text = update.message.text
    historico.append(text)
    if text in CATEGORIAS:
        suboptiones = CATEGORIAS[text]
        #keyboard = [[option] for option in suboptiones] explicar esta opcion para hacerlo mas optimo en los diccionarios
        keyboard = []
        for option in suboptiones:
            keyboard.append([option])
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(f"Seleccionaste {text}. Elige una subcategoría:", reply_markup=reply_markup)
    else:
        await update.message.reply_text(historico)

def main():
    """Configura y ejecuta el bot."""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, option_selected))

    app.run_polling()

if __name__ == "__main__":
    main()