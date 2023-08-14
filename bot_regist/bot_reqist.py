import logging
from aiogram import Bot, Dispatcher, executor, types

from permissions_db import PermissionsDatabase
from config import *

logging.basicConfig(level=logging.INFO)

bot_token = TOKEN_TG
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

users = [USER_ADMIN_ID]
dat = PermissionsDatabase()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    '''
    Приветсвенное сообщение
    '''
    await message.reply("Привет, лишь некоторым доступна темная сила!!!")

@dp.message_handler(commands=['add'])
async def add_users(message: types.Message):
    '''
    Функция для добавления id пользователя в базу данных(Разрешенных пользователей)
    '''
    if message.from_user.id in users:
        id = int(message.text.split(' ')[1])
        if dat.add_id_to_database(id):
            await message.answer('Участник добавлен успешно')
        else:
            await message.answer('Произошла ошибка при добавлении участника')
    else:
        await message.answer("Опа! Ошибочка...")

@dp.message_handler(commands=['delete'])
async def delete_users(message: types.Message):
    '''
    Функция для удаления id пользователя в базу данных(Разрешенных пользователей)
    '''
    if message.from_user.id in users:
        id = int(message.text.split(' ')[1])
        if dat.remove_id_from_database(id):
            await message.answer('Участник успешно удалён')
        else:
            await message.answer('Произошла ошибка при удалении участника')
    else:
        await message.answer("Опа! Ошибочка...")


@dp.message_handler(commands=['watch'])
async def watch_users(message: types.Message):
    '''
    Функция для просмотра id пользователя в базу данных(Разрешенных пользователей)
    '''
    if message.from_user.id in users:
        id = int(message.text.split(' ')[1])
        if dat.check_id_in_database(id):
            await message.answer('Участник добавлен')
        else:
            await message.answer('Участника нет в базе')
    else:
        await message.answer("Опа! Ошибочка...")




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    dat.close_connection()
