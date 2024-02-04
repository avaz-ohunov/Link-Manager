# Bot.py

from aiogram.utils import executor

from reg_bot import dp, bot
from handlers import admin, main
from data_base import database


# Запуск бота
async def on_startup(_):
    await bot.send_message(
        1142268145, 
        "Бот успешно запущен"
    )


# Регистрация обработчиков сообщений
admin.register_handlers_admin(dp)
main.register_handlers_main(dp)

# Регистрация callback обработчиков
admin.register_callback_handlers(dp)


# Работа бота
executor.start_polling(
    dp, skip_updates = True, on_startup = on_startup
)
