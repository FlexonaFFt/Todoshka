#type: ignore
import aiogram
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура для регистрации
registration_button = KeyboardButton(text='Регистрация')

invite_button_grid_not_registrated = ReplyKeyboardMarkup(
    keyboard=[[registration_button]],
    input_field_placeholder='Выберите команду',
    resize_keyboard=True
)

# Основная клавиатура
status_button = KeyboardButton(text='Статус')
menu_button = KeyboardButton(text='Меню')

invite_button_grid_for_registrated = ReplyKeyboardMarkup(
    keyboard=[[status_button], [menu_button]],
    input_field_placeholder='Выберите команду',
    resize_keyboard=True
)

# Вспомогательная клавиатура для ввода номера телефона
auto_phone_button = KeyboardButton(text='Автоматически дать контакт', request_contact=True)

buttons_for_registration = ReplyKeyboardMarkup(
    keyboard=[[auto_phone_button]],
    input_field_placeholder='Выберите команду',
    resize_keyboard=True
)

# Метод для скрытия клавиатуры
buttons_remove = ReplyKeyboardRemove()