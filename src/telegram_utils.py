import pandas as pd
import plotly.graph_objects as go
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from constants import TMP_DIR


async def choose_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send all possible options"""
    file_id = update.message.document.file_id
    file = await context.bot.get_file(file_id)
    df = pd.read_excel(file.file_path)
    # getting user ID
    user_id = update.message.from_user.id
    # mkdir for user
    user_dir = TMP_DIR / str(user_id)
    user_dir.mkdir(exist_ok=True)
    # save new file in user folder
    df.to_excel(user_dir / f"{update.message.message_id}.xlsx")

    possible_comands = ['description', 'box_plots', 'group_comparison']
    urlkb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=command, callback_data=command)]
            for command in possible_comands]
    )
    await update.message.reply_text("вот", reply_markup=urlkb)


def create_graphs(df, graph_name='box_plots'):
    """Create graphs for all columns in df"""
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
    dest = TMP_DIR / f"{graph_name}.html"
    fig.write_html(dest)
    return dest


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    user = update.effective_user
    mes = f"Selected option: {query.data}"
    # load corresponding file
    user_id = update.callback_query.from_user.id
    user_dir = TMP_DIR / str(user_id)
    # choose last filr from user folder
    df = pd.read_excel(sorted(user_dir.glob("*.xlsx"))[-1])
    if query.data == 'description':
        # save description to file
        description_path = user_dir / 'description.xlsx'
        df.describe().to_excel(description_path)
        with open(description_path, 'rb') as iof:
            await query.message.reply_document(iof)
    elif query.data == 'box_plots':
        dest = create_graphs(df)
        with open(dest, 'rb') as iof:
            await query.message.reply_document(iof)
    elif query.data == 'group_comparison':

    mes = "success"
    await query.answer(text=mes)
