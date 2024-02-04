# main_kb.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data_base import database


# Кнопка "+ ссылка"
add_link = InlineKeyboardMarkup().add(
    InlineKeyboardButton(
        text = "+ ссылка🔗",
        callback_data = "+ ссылка🔗"
    )
)

# Кнопки со ссылками
async def links(user_id):
    markup = InlineKeyboardMarkup()
    links = await database.get_links(user_id)
    for link in links:
        markup.insert(InlineKeyboardButton(
            link[0], url = link[1]
        ))

    return markup
