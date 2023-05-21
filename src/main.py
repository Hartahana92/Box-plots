from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import yaml
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, ContextTypes, \
    MessageHandler, filters, CallbackQueryHandler

from src.processing import significant_metabolites, create_graphs
from src.telegram_utils import choose_option, button

config_path = Path(__file__).parent / "config.yaml"
tmp_dir = Path(".tmp")
tmp_dir.mkdir(exist_ok=True)
with open(config_path) as iof:
    config = yaml.load(iof, Loader=yaml.Loader)


# def process_request(bot, update):
#     """Обработка запроса пользователя"""
#     # Получение данных из файла
#     df = pd.read_excel(update.message.document.get_file().download_as_bytearray())
#     # Создание графиков
#     graphs = create_graphs(df)
#     # Отправка графиков пользователю
#     for col, graph in graphs.items():
#         bot.send_message(chat_id=update.message.chat_id, text=f'График для столбца {col}:')
#         bot.send_document(chat_id=update.message.chat_id, document=graph)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n"
        f"Send me a file and I'll send you what I can do with it.\n",
        reply_markup=ForceReply(selective=True),
    )


# async def file_handler(update, context):
#     file = update.message.document.get_file()
#     file.download('file.xlsx')
#     df = pd.read_excel('file.xlsx')
#     update.message.reply_text("я получил файл")


# async def excel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     file_id = update.message.document.file_id
#     file = await context.bot.get_file(file_id)
#     df = pd.read_excel(file.file_path)
#     # getting user ID
#     user_id = update.message.from_user.id
#     # mkdir for user
#     user_dir = TMP_DIR / str(user_id)
#     user_dir.mkdir(exist_ok=True)
#     # save new file in user folder
#     df.to_excel(user_dir / f"{update.message.message_id}.xlsx")
#     # make answer for user with possible commands
#     await update.message.reply_text(
#         "I got your file. What can I do with it?",
#         reply_markup=ForceReply(selective=True),
#     )

    # graphs = create_graphs(df)

    # figures = []
    # for col in df.columns[1:]:
    #     # Создание боксплота
    #     box_plot = go.Box(
    #         x=df['Group'],
    #         y=df[col],
    #         name=col
    #     )
    #     figures.append(box_plot)
    # fig = go.Figure(figures)
    # dest = tmp_dir / f"{update.message.message_id}.html"
    # fig.write_html(dest)
    # excel_tmp_path = tmp_dir / f"{update.message.message_id}.xlsx"
    # significant_metabolites(df).to_excel(excel_tmp_path)
    # await update.message.reply_document(dest)
    # await update.message.reply_document(excel_tmp_path)
    # # with open(dest) as iof:
    # #     await update.message.reply_document(iof)
    # del dest


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config["TELEGRAM_TOKEN"]).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.Document.FileExtension("xlsx"),
                       choose_option)
    )
    application.add_handler(CallbackQueryHandler(button))
    # filters.Document.FileExtension("xlsx")
    #application.add_handler(MessageHandler(filters, start))
    application.run_polling()


if __name__ == '__main__':
    main()
