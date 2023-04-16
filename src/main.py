from pathlib import Path
import yaml
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import telegram
from telegram.ext import Application,CommandHandler,ContextTypes, MessageHandler, filters
from telegram import Update, ForceReply

config_path = Path(__file__).parent / "config.yaml"
tmp_dir = Path(".tmp")
tmp_dir.mkdir(exist_ok=True)
with open(config_path) as iof:
    config = yaml.load(iof, Loader=yaml.Loader)

# Функция для создания графиков из таблицы
def create_graphs(df):
    # Создание пустого словаря для хранения графиков
    graphs = {}
    # Перебор всех столбцов в таблице
    for col in df.columns:
        # Пропуск первого столбца с метками класса
        if col == 'Group':
            continue
        # Создание графика боксплота для каждого столбца
        fig = px.box(df, x='Group', y=col)
        # Сохранение графика в словарь
        graphs[col] = fig.to_html()
    # Возврат словаря с графиками
    return graphs

# Функция для обработки запросов пользователя
def process_request(bot, update):
    # Получение данных из файла
    df = pd.read_excel(update.message.document.get_file().download_as_bytearray())
    # Создание графиков
    graphs = create_graphs(df)
    # Отправка графиков пользователю
    for col, graph in graphs.items():
        bot.send_message(chat_id=update.message.chat_id, text=f'График для столбца {col}:')
        bot.send_document(chat_id=update.message.chat_id, document=graph)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def file_handler(update, context):
    file = update.message.document.get_file()
    file.download('file.xlsx')
    df = pd.read_excel('file.xlsx')
    update.message.reply_text("я получил файл")

async def excel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.document.file_id
    file = await context.bot.get_file(file_id)
    df = pd.read_excel(file.file_path)
    # graphs = create_graphs(df)

    figures = []
    for col in df.columns[1:]:
        # Создание боксплота
        box_plot = go.Box(
            x=df['Group'],
            y=df[col],
            name=col
        )
        figures.append(box_plot)
    fig = go.Figure(figures)
    dest = tmp_dir / f"{update.message.message_id}.html"
    fig.write_html(dest)
    await update.message.reply_document(dest)
    # with open(dest) as iof:
    #     await update.message.reply_document(iof)
    del dest


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config["TELEGRAM_TOKEN"]).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.FileExtension("xlsx"), excel_handler)
                            )

    filters.Document.FileExtension("xlsx")
    #application.add_handler(MessageHandler(filters, start))
    application.run_polling()


if __name__ == '__main__':
    main()
