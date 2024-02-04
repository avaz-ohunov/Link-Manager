# admin_kb.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data_base import database

# Кнопки по умолчанию
main = InlineKeyboardMarkup(row_width = 2).add(
    InlineKeyboardButton(
        text = "+ ссылка🔗",
        callback_data = "+ ссылка🔗"
    ),

    InlineKeyboardButton(
        text = "– ссылка🔗",
        callback_data = "– ссылка🔗"
    )
)

cancel_btn = InlineKeyboardButton(
    text = "Отмена❌",
    callback_data = "Отмена❌"
)

# Кнопка "Отмена"
cancel = InlineKeyboardMarkup().add(cancel_btn)

# Кнопки с именами ссылок
async def links(user_id):
    markup = InlineKeyboardMarkup().row(cancel_btn).row()
    
    links = await database.get_links(user_id)
    for link in links:
        markup.insert(InlineKeyboardButton(
            link[0], callback_data = f"del_{link[0]}"
        ))

    return markup
