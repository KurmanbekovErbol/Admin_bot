from aiogram import types, Bot
from aiogram.filters import CommandStart, Command
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.db import *

router = Router()

from config import token

bot = Bot(token=token)

@router.message(CommandStart())
async def command_start(message: types.Message):
    await message.answer(f"""Здравствуйте {message.from_user.full_name}
Команды для пользователя:
/start - начать.
Команды для админа:
/users - все пользователи бота,
/mailing - рассылка сообщения для всех пользователей бота,
/add_admin - добавление админа в бот,
/remove_admin - понижает админа до пользователя.""")
    register(message.from_user.id, message.from_user.full_name, message.chat.id)

class Mailing(StatesGroup):
    messages = State()

@router.message(Command('mailing'))
async def mailing(message: types.Message, state: FSMContext):
    if check_admins(telegram_id=message.from_user.id) == 1:
        await message.answer("Введите сообщение")
        await state.set_state(Mailing.messages)
    else:
        pass

@router.message(Mailing.messages)
async def mailing_1(message: types.Message, state: FSMContext):
    await state.update_data(messages=message.text)
    await message.answer("Сообщение отправлено")

    data = await state.get_data()
    messages = data["messages"]
    for i in get_chat_id():
        await bot.send_message(i, messages)
    await state.clear()

class Add_admin(StatesGroup):
    add_id = State()

@router.message(Command('add_admin'))
async def add_admin(message: types.Message, state: FSMContext):
    if check_admins(telegram_id=message.from_user.id) == 1:
        await message.answer("Введите id пользователя")
        await state.set_state(Add_admin.add_id)
    else:
        pass

@router.message(Add_admin.add_id)
async def add_admin_1(message: types.Message, state: FSMContext):
    await state.update_data(add_id=message.text)
    if check_admins(telegram_id=message.text) == 0:
        await message.answer("Новый админ добавлен")
        data = await state.get_data()
        add_id = data["add_id"]
        add_admins(add_id)
        await state.clear()
    elif check_admins(telegram_id=message.text) == 1:
        await message.answer("Это пользователь уже является админом")
    else:
        await message.answer("Пользователь не найден")

    

class Remove_admin(StatesGroup):
    remove_admin = State()

@router.message(Command('remove_admin'))
async def remove(message: types.Message, state: FSMContext):
    if check_admins(telegram_id=message.from_user.id) == 1:
        await message.answer("Введите id админа")
        await state.set_state(Remove_admin.remove_admin)
    else:
        pass

@router.message(Remove_admin.remove_admin)
async def remove_1(message: types.Message, state: FSMContext):
    await state.update_data(remove_admin=message.text)
    if check_admins(telegram_id=message.text) == 1:
        await message.answer("Админ понижен до пользователя")
        data = await state.get_data()
        remove_admin = data["remove_admin"]
        demote_admin(remove_admin)
        await state.clear()
    elif check_admins(telegram_id=message.text) == 0:
        await message.answer("Это пользователь а не админ")
    else:
        await message.answer("Пользователь не найден")



@router.message(Command('users'))
async def all_users(message: types.Message):
    if check_admins(message.from_user.id) == 1:
        await message.answer('Все пользователи бота:')
        for i in get_users():
            await message.answer(f"{i}")
    else:
        pass



