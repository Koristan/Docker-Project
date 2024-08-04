from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.markdown import hlink
import requests
import config
import keyboards
import json

router = Router()
need_answer = False
need_alt_answer = False
page_num = 1
pagination = 3
max_messages = 0

@router.message(F.text.lower() == "/start")
async def start_handler(msg: Message):
    global page_num
    page_num = 1
    keyboard = keyboards.create_keyboard(['Оставить новое сообщение', 'Просмотреть все сообщения'])

    await msg.answer("Добро пожаловать! Что вы хотите сделать?", reply_markup=keyboard)


@router.message(F.text.lower() == "просмотреть все сообщения")
async def get_messages(msg : Message):
    global need_alt_answer
    global page_num
    global pagination
    global max_messages
    max_count = pagination * page_num
    min_count = (pagination * page_num) - pagination
    count = 0
    messages = requests.get(url=f'{config.BASE_URL}/api/v1/messages')
    decoded_message = json.loads(messages.text)
    max_messages = len(decoded_message)
    need_alt_answer = True
    for message_id in decoded_message:
        if count <= max_count and count >= min_count:
            name = decoded_message[message_id]['name']
            text = decoded_message[message_id]['message']

            keyboard = keyboards.create_keyboard(['Назад','<', '>'])
            print(count, page_num)
            await msg.answer(f"Оставлен: {name}\n{text}", reply_markup=keyboard)
        count += 1

@router.message(F.text.lower() == "оставить новое сообщение")
async def post_message(msg : Message):
    global need_answer
    need_answer = True
    await msg.answer("Какое сообщение оставите?")
   

@router.message()
async def message_handler(msg: Message):
    global need_answer
    global need_alt_answer

    global page_num
    global pagination
    global max_messages

    if need_answer:
        name = msg.from_user.username
        need_answer = False
        
        requests.post(url=f'{config.BASE_URL}/api/v1/message?name={name}&message_text={msg.text}',)

        keyboard = keyboards.create_keyboard(['/start'])
        await msg.answer(f"Отлично! Сообщение оставлено!", reply_markup=keyboard)

    elif need_alt_answer:
        
        if (msg.text.lower() == '<'):
            if (page_num != 1):
                page_num -= 1
                await get_messages(msg)
            else:
                await msg.answer("Это и так начало.")
        elif (msg.text.lower() == '>'):
            if (page_num < (max_messages/pagination)):
                page_num += 1
                await get_messages(msg)
            else:
                await msg.answer("Комментариев больше нет...")
        else:
            await start_handler(msg)
            need_alt_answer = False
            

    else:

        keyboard = keyboards.create_keyboard(['/start'])
        await msg.answer(f"Попробуй /start", reply_markup=keyboard)