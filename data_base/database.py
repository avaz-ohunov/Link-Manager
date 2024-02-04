# database.py

import aiosqlite

from reg_bot import bot


# Создание таблицы для пользователя
async def start(user_id):
	async with aiosqlite.connect("links.db") as db:
		await db.execute(
			"""CREATE TABLE IF NOT EXISTS user{}(
										title TEXT, 
										link TEXT
			)""".format(user_id)
		)

		await db.commit()


# Добавление ссылок в БД
async def add_link(user_id, state):
	async with state.proxy() as data:
		async with aiosqlite.connect("links.db") as db:
			await db.execute(
				"INSERT INTO user{} VALUES(?, ?)".format(user_id),
				tuple(data.values())
			)

			await db.commit()


# Удаление ссылок из БД
async def delete_link(user_id, title):
	async with aiosqlite.connect("links.db") as db:
		await db.execute(
			"DELETE FROM user{} WHERE title == ?".format(user_id),
			(title,)
		)

		await db.commit()


# Получение ссылок
async def get_links(user_id):
	async with aiosqlite.connect("links.db") as db:
		cursor = await db.execute(
			"SELECT * FROM user{}".format(user_id)
		)
		
		links = await cursor.fetchall()
		await cursor.close()
		
		return links
