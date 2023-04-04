import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from generator import generate_long_answer
from users_db import get_question_for, increase_number_right_answers, get_stat_user, \
    insert_mes_id, get_mes_id, increase_number_asked, set_question_theme

API_TOKEN = 'Your token'


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


async def send_question(user, dp: Dispatcher):

    await del_mess(user, dp)
    question = get_question_for(user)

    quest = question['question'] + '\n'
    right_answer = question['answer']
    list_of_answers = list({right_answer, question['var1'], question['var2']})

    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)

    for i, var in enumerate(list_of_answers):

        text_and_data = ((str(i + 1), 'True' if var == right_answer else 'False'),)
        row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
        keyboard_markup.row(*row_btns)

        quest += str(i + 1) + ') ' + var + '\n'

    mes = await bot.send_message(user, quest, reply_markup=keyboard_markup)
    insert_mes_id(user, mes.message_id)

    @dp.callback_query_handler()
    async def inline_kb_answer_callback_handler(query: types.CallbackQuery, state: FSMContext):
        answer_data = query.data
        await query.message.delete()
        await del_mess(query.from_user.id, dp)
        text_mes = ''
        if answer_data == 'next':
            await send_question(query.from_user.id, dp)
        elif answer_data == 'theme':
            await bot.send_message(query.from_user.id, 'Write new theme')
            # States
            class Form_mes(StatesGroup):
                theme = State()
            await Form_mes.theme.set()
            @dp.message_handler(state=Form_mes.theme)
            async def scan_message(message: types.Message, state: FSMContext):
                set_question_theme(message.from_user.id, message.text)
                await bot.send_message(message.from_user.id, 'Theme changed')
                await state.finish()
                await send_question(message.from_user.id, dp)
        else:
            increase_number_asked(query.from_user.id)
            if answer_data == 'True':
                text_mes = 'True!\n'
                increase_number_right_answers(query.from_user.id)
            elif answer_data == 'False':
                text_mes = 'False!\n'


            stat = get_stat_user(query.from_user.id)
            text_mes += f'Wright answers: {stat["number_of_right_answers"]} z {stat["asked"] + 1}\n'
            text_mes += stat['question']

            keyboard_markup = types.InlineKeyboardMarkup(row_width=1)

            text_and_data = (('Next question', 'next'),)
            row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
            keyboard_markup.row(*row_btns)

            text_and_data = (('New theme', 'theme'),)
            row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
            keyboard_markup.row(*row_btns)

            logging.info(f'{query.from_user.id}, {text_mes}')
            mes = await bot.send_message(query.from_user.id, text_mes, reply_markup=keyboard_markup)
            insert_mes_id(query.from_user.id, mes.message_id)


async def del_mess(user, dp: Dispatcher):
    try:
        mess_id = get_mes_id(user)
        await bot.delete_message(user, mess_id)
    except Exception as e:
        print(f'can not delete message for {user}: {e}')


