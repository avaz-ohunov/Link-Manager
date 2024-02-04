# admin.py

import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher

from reg_bot import dp, bot
from data_base import database
from keyboards import admin_kb, main_kb


# Добавление ссылок
class AddLink(StatesGroup):
	get_link_title = State()
	get_link = State()

# Удаление ссылок
class DeleteLink(StatesGroup):
	delete_link = State()


# Функция для отправки состояния печати
async def bot_typing(user_id, time):
	await bot.send_chat_action(
		user_id,
		types.ChatActions.TYPING
	)

	await asyncio.sleep(time)


# Панель администратора
async def admin_panel(message: types.Message):
	await bot_typing(message.from_user.id, 1)
	await message.answer(
		"Панель администратора👇",
		reply_markup = admin_kb.main
	)


# Отмена состояния
async def cancel(callback: types.CallbackQuery, state: "*"):
	await callback.message.edit_reply_markup(reply_markup = None)

	await state.reset_state()
	await bot_typing(callback.from_user.id, 1)
	await callback.message.answer(
		"Главное меню",
		reply_markup = admin_kb.main
	)


# Обработка команды "+ ссылка"
async def command_add_link(callback: types.CallbackQuery, state: AddLink):
	await callback.message.edit_reply_markup(reply_markup = None)

	await bot_typing(callback.from_user.id, 2)
	await callback.message.answer(
		"Введите название ссылки🔗",
		reply_markup = admin_kb.cancel
	)

	await AddLink.get_link_title.set()


# Получение названия ссылки
async def get_link_title(message: types.Message, state: AddLink):
	async with state.proxy() as data:
		data["link_title"] = message.text

	await bot_typing(message.from_user.id, 2)
	
	await message.answer(
		"Пришлите саму ссылку🔗",
		reply_markup = admin_kb.cancel
	)

	await AddLink.get_link.set()


# Добавление ссылки
async def get_link(message: types.Message, state: AddLink):
	async with state.proxy() as data:
		data["link"] = message.text

	await database.add_link(message.from_user.id, state)
	await bot_typing(message.from_user.id, 1)
	
	await message.answer(
		"Ссылка добавлена✅",
		reply_markup = admin_kb.main
	)

	await state.finish()


# Обработка команды "– ссылка"
async def command_delete_link(callback: types.CallbackQuery, state: DeleteLink):
	await callback.message.edit_reply_markup(reply_markup = None)

	del_links = await admin_kb.links(callback.from_user.id)

	if del_links["inline_keyboard"][1] == []:
		await bot_typing(callback.from_user.id, 1)
		await callback.message.answer(
			"Удалять нечего",
			reply_markup = main_kb.add_link
		)

		await asyncio.sleep(0.5)
		await callback.message.answer_sticker("CAACAgIAAxkBAAILz2W_8ik-Yyr_dcsFiY5vXB8QIowFAAKQAQACMNSdEUqG5uIJ-atJNAQ")

		return

	await bot_typing(callback.from_user.id, 3)

	await callback.message.answer(
		"Кликните на ссылку🔗, которую хотите удалить❌",
		reply_markup = del_links
	)

	await DeleteLink.delete_link.set()


# Удаление ссылки
async def delete_link(callback: types.CallbackQuery, state: DeleteLink):
	await callback.message.edit_reply_markup(reply_markup = None)

	link_title = callback.data.split("_")[1]
	await database.delete_link(callback.from_user.id, link_title)
	await bot_typing(callback.from_user.id, 1)
	await callback.message.answer(
		"Ссылка удалена❌",
		reply_markup = admin_kb.main
	)

	await state.finish()


# Регистрация хендлеров сообщений админа
def register_handlers_admin(dp: Dispatcher):
	dp.register_message_handler(
		admin_panel, commands = ["admin"]
	)

	dp.register_message_handler(
		get_link_title, state = AddLink.get_link_title
	)

	dp.register_message_handler(
		get_link, state = AddLink.get_link
	)


# Регистрация callback-хендлеров
def register_callback_handlers(dp: Dispatcher):
	dp.register_callback_query_handler(
		cancel, text = "Отмена❌", state = "*"
	)

	dp.register_callback_query_handler(
		command_add_link, text = "+ ссылка🔗"
	)

	dp.register_callback_query_handler(
		command_delete_link, text = "– ссылка🔗"
	)

	dp.register_callback_query_handler(
		delete_link, 
		lambda callback: callback.data.startswith("del_"),
		state = DeleteLink
	)
