import logging

from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from afunc import send_question
from users_db import create_users_base, new_user

API_TOKEN = 'Your token'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger('broadcast')
logging.info('_____________________________________________________________________________________________')
create_users_base()


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    logging.info(datetime.now())
    logging.info(message)
    new_user(message.from_user.id)
    await send_question(message.from_user.id, dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
