import logging
from time import sleep

from telegram import __version__ as TG_VER
import conf.conf_bot

from telegram import ForceReply, Update

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import ext.database_ext as db_ext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! {user.id}",
        reply_markup=ForceReply(selective=True),
    )
    # await update.message.reply_document(
    #     document=open("../README.md", "rb"),
    #     caption=f"Hi {user.mention_html()}! I'm {context.bot.first_name}.\n\n"
    #             f"Telegram Bot API version: {TG_VER}\n"
    # )


async def send_all_doc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    all_brosur = db_ext.get_data_db()
    for brosur in all_brosur:
        logger.info(f"Send Brosur {brosur.title} -- {brosur.size}")
        await update.message.reply_document(
            document=open("download/" + brosur.title + ".pdf", "rb"),
            caption=f"Judul: {brosur.title}\n"
                    f"Tanggal: {brosur.date_create}\n"
                    f"Size: {brosur.size}\n"
        )
        sleep(1)

    # await update.message.reply_document(
    #     document=open("../README.md", "rb"),
    #     caption=f"Hi {user.mention_html()}! I'm {context.bot.first_name}.\n\n"
    #             f"Telegram Bot API version: {TG_VER}\n"
    # )
    # await update.message.reply_text("Help!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(conf.conf_bot.TOKEN).build()
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("send_all_doc", send_all_doc))
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
