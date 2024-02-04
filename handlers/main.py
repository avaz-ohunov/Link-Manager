# main.py

import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher

from reg_bot import dp, bot
from data_base import database
from keyboards import main_kb


# Функция для отправки состояния печати
async def bot_typing(user_id, time):
    await bot.send_chat_action(
        user_id,
        types.ChatActions.TYPING
    )

    await asyncio.sleep(time)


# Обработка команды /start
async def start(message: types.Message):
    await database.start(message.from_user.id)
    await bot_typing(message.from_user.id, 3)
    await message.answer(
        f"Приветствую Вас, {message.from_user.first_name}! "
        "Добавьте свою первую ссылку🔗",
        reply_markup = main_kb.add_link
    )

    await asyncio.sleep(0.5)
    await message.answer_sticker("CAACAgIAAxkBAAILyGW_79Se78GoBE_W-rA3qrnWwLo0AAKgAQACMNSdEYM014Zyl9YTNAQ")


# Обработка команды /restart
async def restart(message: types.Message, state: "*"):
    await state.reset_state()
    await bot_typing(message.from_user.id, 1)
    await message.answer("Ура! Я перезапущен🔄")
    await asyncio.sleep(0.5)
    await message.answer_sticker("CAACAgIAAxkBAAILymW_8UIm5BsiwAxdBzIlKz5Q0jsuAAKoAQACMNSdEQ9mlBNu5v_eNAQ")


# Бот присылает ссылки пользователя в ответ на любое его сообщение
async def your_links(message: types.Message):
    links = await main_kb.links(message.from_user.id)
    
    if links["inline_keyboard"] == []:
        await bot_typing(message.from_user.id, 3)
        await message.answer(
            "У вас ещё нет ссылок, добавьте свою первую ссылку🔗",
            reply_markup = main_kb.add_link
        )
    
    else:
        await bot_typing(message.from_user.id, 1)
        await message.answer(
            "Ваши ссылки🔗",
            reply_markup = links
        )


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(start, commands = ["start"])
    dp.register_message_handler(restart, commands = ["restart"])
    dp.register_message_handler(your_links)
