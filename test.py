import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.handlers.basic import start_cmd

bot = Bot(token = '7610953420:AAFJSJneepus_P5BYdeHolzEEOK-8jA107g')

dp = Dispatcher() #Класс, который обрабатывает сообщения


# button1 = KeyboardButton(text="Кнопка 1")
# button2 = KeyboardButton(text="Кнопка 2")

# # Создаем клавиатуру
# reply_keyboard = ReplyKeyboardMarkup(
#     keyboard=[[button1, button2]],
#     resize_keyboard=True
# )







@dp.message()
async def reply_to_buttons(message: types.Message):
    if message.text == "💳 Заказать":
        await message.answer(" dsads")
    elif message.text == "ℹ️ Помощь":
        await message.answer("У меня всё хорошо, а у тебя? 😉")
    elif message.text == "📃 Список":
        
        # categories = types.InlineKeyboardMarkup(row_width=1)
        strenght = InlineKeyboardButton(text='Крепкость', callback_data='strenght')
        Taste = InlineKeyboardButton(text='Вкус', callback_data='xyi')
        Brand = types.InlineKeyboardButton(text='Название Линейки', callback_data='brand')
        alle = types.InlineKeyboardButton(text='Все товары', callback_data='alle')
        
        reply_categories = InlineKeyboardMarkup(
        inline_keyboard=[[strenght],[Taste],[Brand] ,[alle ]],
        resize_keyboard=True# Правильная структура
        )
        
        await message.answer("Выберите категорию товара!", reply_markup = reply_categories)

    elif message.text == "💻 Профиль":
        await message.answer("У меня всё хорошо, а у тебя? 😉")
    else:
        await message.answer("Я не понимаю 😕 Выбери кнопку из меню.")




    
# Обработчик команды /menu
@dp.message(Command("menu"))
async def menu_cmd(message: types.Message):

    button1 = KeyboardButton(text="Кнопка 1")
    button2 = KeyboardButton(text="Кнопка 2")

    # Создаем клавиатуру
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[[button1, button2]],  # Это правильный формат
        resize_keyboard=True
    )
    await message.answer('Выберите:', reply_markup=reply_keyboard)
    
    
@dp.message(Command("inline"))
async def inline_btn(message: types.Message):
    button1 = InlineKeyboardButton(text="Кнопка 1", callback_data="btn_1")
    button2 = InlineKeyboardButton(text="Кнопка 2", callback_data="btn_2")

    # Создаем инлайн клавиатуру
    reply_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[button1, button2]]  # Правильная структура
    )
    await message.answer('Выберите:', reply_markup=reply_keyboard)
    
@dp.message(~ (F.text.contains('проверка'))) # Как message handler
async def strt_cmd(message: types.Message):
    await message.answer( 'Укажите текст с проверкой!')

@dp.message() # Как message handler
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, '*Ответ*', parse_mode = 'Markdown') # Одинаково
    await message.answer(message.text) # Одинаково
    await message.reply('Ответ на сообщение')
    
    



async def main():
    await bot.delete_webhook(drop_pending_updates=True) #Не будет обрабытывать сообщение, отправленные, когда бот был не в сети
    await dp.start_polling(bot) #Запуск бота
    
    
if __name__ == "__main__":
    asyncio.run(main())