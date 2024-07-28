#type: ignore
import os
import base64
import asyncio
import requests
from aiogram import F
import keyboards as kb
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
from database import Database


class TelegramBot:
    def __init__(self, token):
        self.bot = Bot(token)
        self.dp = Dispatcher(storage=MemoryStorage())

    def start_polling(self):
        self.dp.run_polling(self.bot)


class TelegramFunctions:
    class RegistrationState(StatesGroup):
        phone_number = State()
        firstname = State()
        response = State()

    def __init__(self, dp, bot):
        self.dp = dp
        self.bot = bot
        self.db = Database('my_database.db')  # Создаем экземпляр базы данных

    def setup_handlers(self):
        @self.dp.message(CommandStart())
        async def start_command(message: types.Message):
            user = self.db.get_user_by_username(message.from_user.username)
            try:
                if user:
                    await message.answer("Привет! Это бот на aiogram и SQLite. \n\nИспользуйте команду 'Статус' для проверки статуса или 'меню', чтобы открыть меню.", \
                        reply_markup=kb.invite_button_grid_for_registrated)
                else:
                    await message.answer("Вам необходимо зарегистрироваться в боте, для этого нажмите на кнопку 'Регистрация'",\
                        reply_markup=kb.invite_button_grid_not_registrated)
            except Exception as e:
                await message.answer(f"Что-то пошло не так. Попробуйте ещё раз позже. Ошибка: {str(e)}")

        @self.dp.message(F.text.lower() == 'регистрация')
        async def register_command(message: types.Message, state: FSMContext):
            user = self.db.get_user_by_username(message.from_user.username)
            try:
                if user:
                    await message.answer("Вы уже зарегистрированы!")
                else:
                    await state.set_state(self.RegistrationState.phone_number)
                    await message.answer("Пожалуйста, отправьте ваш номер телефона или воспользуйтесь автоматическим вводом.", \
                        reply_markup=kb.buttons_for_registration)
            except Exception as e:
                await message.answer(f"Что-то пошло не так. Попробуйте ещё раз позже. Ошибка: {str(e)}")

        @self.dp.message(self.RegistrationState.phone_number)
        async def process_phone_number(message: types.Message, state: FSMContext):
            try:
                if message.text.lower() == 'автоматически дать контакт':
                    await state.update_data(phone_number=message.contact.phone_number)
                    await state.set_state(self.RegistrationState.firstname)
                    await message.answer("Пожалуйста, отправьте ваше имя.")
                else:
                    await message.answer("Это не похоже на ваш номер телефона :( \n Попробуйте ввести его вручную")
                    await state.set_state(self.RegistrationState.phone_number)
            except:
                await state.update_data(phone_number=message.text)
                await state.set_state(self.RegistrationState.firstname)
                await message.answer("Пожалуйста, отправьте ваше имя")

        @self.dp.message(self.RegistrationState.firstname)
        async def process_firstname(message: types.Message, state: FSMContext):
            try:
                await state.update_data(firstname=message.text)
                await message.answer("Отлично, осталось лишь узнать ваш адрес. \n\nПожалуйста, в точности напишите свой адрес с точностью до улицы.\n\nЕсли ваш адрес 'г. Елабуга, проспект Нефтяников, д. 125'\nТо необходимо написать: Нефтяников 125.", \
                    reply_markup=kb.buttons_remove)
                await state.set_state(self.RegistrationState.adress)
            except:
                await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.") 

        @self.dp.message(self.RegistrationState.response)
        async def process_request(message: types.Message, state: FSMContext):
            try:
                data = await state.get_data()
                adress = data['adress']
                phone_number = data['phone_number']
                firstname = data['firstname']
                username = message.from_user.username

                if message.text.lower() == 'подтвердить':
                    self.db.add_user(phone_number, username, firstname, adress)
                    await message.answer("Вы успешно зарегистрированы!", reply_markup=kb.invite_button_grid_for_registrated)
                    print("Регистрация пользователя прошла успешно!")
                    await state.clear()
                else:
                    await message.answer('Пожалуйста, подтвердите адрес')
            except:
                await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.")

        @self.dp.message(F.text.lower() == 'статус')
        async def status_command(message: types.Message):
            try:
                user = self.db.get_user_by_username(message.from_user.username)
                if user:
                    await message.answer("Вы зарегистрированы!")
                else:
                    await message.answer("Вы не зарегистрированы!")
            except:
                await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.")

    def close(self):
        self.db.close()  # Закрываем соединение с базой данных


if __name__ == '__main__':
    if not BOT_TOKEN:
        exit("Ошибка TELEGRAM_BOT_TOKEN in env variable")

    bot = TelegramBot(BOT_TOKEN)
    functions = TelegramFunctions(bot.dp, bot.bot)
    functions.setup_handlers()
    try:
        bot.start_polling()
    finally:
        functions.close()  # Закрываем соединение с базой данных