import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import *
from aiogram.fsm.storage.memory import MemoryStorage

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage: MemoryStorage = MemoryStorage()

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Создаем "базу данных" пользователей
    user_dict: dict[int, dict[str, str | int | bool]] = {}

    # Регистриуем роутеры в диспетчере
    dp.include_router(system_handlers.router)
    dp.include_router(send_photo_handlers.router)
    dp.include_router(move_handlers.router)
    dp.include_router(new_risk_handlers.router)
    dp.include_router(elimination_risk_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        # Запускаем функцию main в асинхронном режиме
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Bot stopped!')