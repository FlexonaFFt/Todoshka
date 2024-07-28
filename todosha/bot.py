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
        self.db = Database('my_database.db')

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
                if F.text.lower() == 'автоматически дать контакт':
                    try:
                        await state.update_data(phone_number=message.contact.phone_number)
                        await state.set_state(self.RegistrationState.firstname)
                        await message.answer("Пожалуйста, отправьте ваше имя.")
                    except:
                        await message.answer("Это не похоже на ваш номер телефона :( \n Попробуйте ввести его вручную")
                        await state.set_state(self.RegistrationState.phone_number)
                else:
                    await state.update_data(phone_number=message.text)
                    await state.set_state(self.RegistrationState.firstname)
                    await message.answer("Пожалуйста, отправьте ваше имя")
            except:
                await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.")

        @self.dp.message(self.RegistrationState.firstname)
        async def process_firstname(message: types.Message, state: FSMContext):
            try:
                await message.answer("Отлично, осталось лишь подвердить точность этих данных. Вы уверены что правильно указали данные? Если да, нажмите подтвердить. Если хотите изменить введённые данные, перезапустите бота и пройдите процедуру заново.", \
                    reply_markup=kb.buttons_for_confirmation)
                await state.set_state(self.RegistrationState.response)
            except:
                await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.") 

        @self.dp.message(self.RegistrationState.response)
        async def process_request(message: types.Message, state: FSMContext):
            #try:
                data = await state.get_data()
                phone_number = data.get('phone_number')
                firstname = data.get('firstname')
                username = message.from_user.username

                if message.text.lower() == 'подтвердить':
                    self.db.add_user(phone_number, username, firstname)
                    await message.answer("Вы успешно зарегистрированы!", reply_markup=kb.invite_button_grid_for_registrated)
                    print("Регистрация пользователя прошла успешно!")
                    await state.clear()
                else:
                    await message.answer('Пожалуйста, подтвердите данные')
            #except:
                #await message.answer("Что-то пошло не так. Попробуйте ещё раз позже.")

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