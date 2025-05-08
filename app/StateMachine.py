
import asyncio

from aiogram import F, Router
from aiogram.types import Message 
from aiogram.filters import  Command
from aiogram.types import  CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

import app.keyboard as kb 
import app.database.request as rq

router1 = Router()

    

class NewItem(StatesGroup):
    name = State()
    strenght = State()
    taste = State()
    description = State()
    price = State()
    quantity = State()
    category = State()
    next_state = State()

class Bonus(StatesGroup):
    name = State()
    
class Broadcast(StatesGroup):
    text = State()
        
@router1.callback_query(F.data == "addProduct")
async def newitem(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    chekadmin = await rq.chekAdmin(tg_id = user_id)
    if chekadmin:
        await state.set_state(NewItem.name)
        await callback.message.answer('🖌 Добавление товара! Пожалуйста укажите название')
    else:
        await callback.answer("Эта команда вам не доступна...")

@router1.message(Command("newitem")) # Машина состояния
async def newitem(message: Message, state: FSMContext):
    user_id = message.from_user.id
    chekadmin = await rq.chekAdmin(tg_id = user_id)
    if chekadmin:
        await state.set_state(NewItem.name)
        await message.answer('🖌 Добавление товара! Пожалуйста укажите название')
    else:
        await message.answer("Эта команда вам не доступна...")
    
        
@router1.message(NewItem.name)
async def notName(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(NewItem.strenght)
    await message.answer('Укажите крепкость товара!')
    
@router1.message(NewItem.strenght) 
async def notText(message: Message, state: FSMContext):
    await state.update_data(strenght=message.text)
    await state.set_state(NewItem.taste)
    await message.answer('Укажите вкус товара!')
    
@router1.message(NewItem.taste) 
async def notText(message: Message, state: FSMContext):
    await state.update_data(taste=message.text)
    await state.set_state(NewItem.description)
    await message.answer('Добавьте описание к товару')

@router1.message(NewItem.description) 
async def notText(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(NewItem.price)
    await message.answer('Укажите цену товара!')
    
@router1.message(NewItem.price) 
async def notText(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(NewItem.quantity)
    await message.answer('Укажите колличество товара!')
    
@router1.message(NewItem.quantity) 
async def notText(message: Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    await state.set_state(NewItem.category)
    await message.answer('Выберите категорию и отправьте цифрой!')
    
@router1.message(NewItem.category) 
async def notText(message: Message, state: FSMContext):
    if message.text in ['1', '2', '3', '4']:
        await state.update_data(category=message.text)
        await message.answer("✅ Категория сохранена.")
        
        data = await state.get_data()
        await rq.new_item(
            name=data["name"],
            strenght=data["strenght"],
            taste=data["taste"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"],
            category=data["category"]
            # category по умолчанию = 1
        )
        
        await rq.additem_toAll(
            name=data["name"],
            strenght=data["strenght"],
            taste=data["taste"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"])
    
        await state.clear()
        # Тут можно перейти к следующему шагу
        # await state.set_state(NewItem.next_state)
    elif message.text == '2609':
        await message.answer('❗ Пожалуйста, выберите число категории от 1 до 4.')
        await state.set_state(NewItem.next_state)
    else:
        await message.answer('❗ Пожалуйста, выберите число категории от 1 до 4.')
        # состояние остаётся NewItem.category, так что обработчик вызовется снова
        
@router1.message(NewItem.category) 
async def notText(message: Message, state: FSMContext):
    if message.text in ['1', '2', '3', '4']:
        await state.update_data(category=message.text)
        
@router1.callback_query(F.data == "sendall")
async def broadcast(callback: CallbackQuery, state: FSMContext):
        await callback.message.answer("Пожалуйста введите текст, для массовой рассылки!")
        await state.set_state(Broadcast.text)

@router1.message(Broadcast.text)
async def broadcast(message: Message, state: FSMContext):
    x = 0
    await state.update_data(text=message.text)
    await message.answer("📤 Рассылка началась...")
    
    data = await state.get_data()
    
    user_ids = await rq.broadcast_users()
    for user_id in user_ids:
        try:
            x = x + 1
            await message.bot.send_message(user_id, "📢 Внимание! "
                            "Вы получили это сообщение, потому что подписаны на нашего бота. "
                            "Сейчас начинается новая рассылка с важной информацией. "
                            f"Пожалуйста, ознакомьтесь с сообщением ниже.\n\n <code> {data["text"]}</code>", parse_mode='HTML')
            await asyncio.sleep(0.05)
        except (TelegramForbiddenError, TelegramBadRequest):
            print(f"Ошибка при отправке {user_id}")
    
    await message.answer(f"✅ Рассылка завершена. Всего сообщений отправленно {x} пользователям!")
    
    await state.clear()
    
@router1.callback_query(F.data == "cupon")
async def bonus(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🎁 _Для активации купона введите его название:_", parse_mode='Markdown')
    await state.set_state(Bonus.name)
    
@router1.message(Bonus.name)
async def Bous(message: Message,state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    
    text = data["name"]
    user = message.from_user.id
    
    
    setting = await rq.set_bonuce(text, user)
    
    if setting:
        await message.answer("✅ Бонус успешно активирован!")
    else: 
        await message.answer("Еще нету такого бонуса или превышено колл-во использований...")
        
    await state.clear()