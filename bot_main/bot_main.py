import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from text_recognition import recognition_eng_and_rus
from GPT_english_task import chat_work
from statistics_db import * 
from get_permission_db import *
from config import TOKEN_TG

logging.basicConfig(level=logging.INFO)

bot_token = TOKEN_TG
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dat_st = DatabaseStatistics()
dat_pr = DatabasePer()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    '''
    Функция приветствия и проверка пользоваеля в базе
    '''
    if not dat_st.check_id_in_stat_database(message.from_user.id):
        dat_st.add_id_to_database(message.from_user.id)
    await message.answer("Привет! Этот бот поможет тебе выполнить задание по английскому загружай фото или пиши своё задание!!")


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def save_photo(message: types.Message):
    '''
    Функция для обработки фото-сообщения. Распознавание текста и обработка CHATGPT
    '''
    if dat_st.get_requests_count(message.from_user.id) is None:
        await message.answer('Для регестрации введите команду /start')
    elif dat_pr.check_id_in_database(message.from_user.id) or (int(dat_st.get_requests_count(message.from_user.id)) < 10 and dat_st.get_requests_count(message.from_user.id) is not None):
        photo = message.photo[-1]
        photo_id = photo.file_id

        file_path = f'{photo_id}.jpg'
        await bot.download_file_by_id(photo_id, file_path)
        text = recognition_eng_and_rus(f'{photo_id}.jpg')
        await message.reply("Изображение сохранено!")
        await message.answer("Формируем ответ...")
        try:
            answer = chat_work(text)
        except Exception:
            await message.answer("Упс!! Повтори запрос через некторое время")
        os.remove(file_path)
        await message.answer(answer)
        dat_st.increment_requests_count(message.from_user.id)
    else:
        await message.answer('Упс! Лимит беcплатного использования закончен, обратитеbсь к менеджеру ')


@dp.message_handler(content_types=["text"])
async def do_something(message: types.Message):
    '''
    Функция получает текст от пользователя, обрабатывается при помощи ChatGPT, и отправляет ответ
    '''
    if dat_st.get_requests_count(message.from_user.id) is None:
        await message.answer('Для регестрации введите команду /start')
    elif dat_pr.check_id_in_database(message.from_user.id) or int(dat_st.get_requests_count(message.from_user.id)) < 10:
        await message.answer("Формируем ответ...")
        try:
            answer = chat_work(message.text)
        except Exception:
            await message.answer("Упс!! Повтори запрос через некторое время")
        await message.answer(answer)
        dat_st.increment_requests_count(message.from_user.id)
    else:
        await message.answer('Упс! Лимит беcплатного использования закончен, обратитесь к менеджеру ')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
