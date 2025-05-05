from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.database.request import get_categories, get_category_item, get_categories2

from aiogram.utils.keyboard import InlineKeyboardBuilder

btnOrder = KeyboardButton(text = '💳 Заказать')
btnList = KeyboardButton(text = '📃 Список')
btnHelp = KeyboardButton(text = 'ℹ️ Помощь')
btnProfile = KeyboardButton(text = '💻 Профиль')
btnApanel = KeyboardButton(text = '💻 Админ Панель')


add = InlineKeyboardButton(text='💳Пополнить', callback_data='add')
mybuy = InlineKeyboardButton(text='🛒Мои покупки', callback_data='myBuy')
referal = InlineKeyboardButton(text='🗣Реферальная система', callback_data='referal')
cupon = InlineKeyboardButton(text='🎁Активировать купон', callback_data='cupon')

back = InlineKeyboardButton(text="🔙 Назад", callback_data="menu_main")
order = InlineKeyboardButton(text="💳 Заказать", callback_data="strengt_main")
back1 = InlineKeyboardButton(text="🔙 Назад", callback_data="strengt_main")
back2 = InlineKeyboardButton(text="🔙 Назад", callback_data="taste_main")

st1 = InlineKeyboardButton(text='💥 Low (16-20mg)', callback_data='low')
st2 = InlineKeyboardButton(text='💥 Medium (35-50mg)', callback_data='medium')
st3 = InlineKeyboardButton(text='💥 High (60-75mg)', callback_data='high')
st4 = InlineKeyboardButton(text='💥 Extra High (160mg)', callback_data='extra')

fruits = InlineKeyboardButton(text='🫐 Фрукты и Ягоды', callback_data='fruit')
mint = InlineKeyboardButton(text='🌬 Мята', callback_data='mint')
other = InlineKeyboardButton(text='🛒 Остальное', callback_data='other')

strenght = InlineKeyboardButton(text='Крепкость', callback_data='strenght')
Taste = InlineKeyboardButton(text='Вкус', callback_data='taste')
Brand = InlineKeyboardButton(text='Название Линейки', callback_data='brand')
alle = InlineKeyboardButton(text='Все товары', callback_data='alle')

cb = InlineKeyboardButton(text='✅Получить', callback_data='call')
callback1 = InlineKeyboardButton(text='➡️Пропустить', callback_data='call2')

add = InlineKeyboardButton(text='💳 Пополнить', callback_data='call')
myBuy = InlineKeyboardButton(text='💳 Пополнить', callback_data='call')

bck = InlineKeyboardButton(text='🔙 Назад', callback_data="go_back")
buy = InlineKeyboardButton(text='💰 Купить товар', callback_data="go_back")

users = InlineKeyboardButton(text='Список пользователей', callback_data="usersList")
newsletter = InlineKeyboardButton(text='Масс. Рассылка', callback_data="sendall")
orders= InlineKeyboardButton(text='Заказы', callback_data="orders")
categorieAdding = InlineKeyboardButton(text='Добавить категорию', callback_data="addCategory")
productAdding= InlineKeyboardButton(text='Добавить товар', callback_data="addProduct")

user_keyboard = ReplyKeyboardMarkup(keyboard=[[btnOrder, btnList],
                                     [btnHelp],
                                     [btnProfile]], resize_keyboard=True)

reply_apanel = ReplyKeyboardMarkup(keyboard=[[btnList, btnHelp],
                                            [btnApanel],[btnProfile]], resize_keyboard=True)

reply_categories = InlineKeyboardMarkup(
inline_keyboard=[[strenght],[Taste],[Brand] ,[alle]],
resize_keyboard=True# Правильная структура
)

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [back]
])

apanel = InlineKeyboardMarkup(inline_keyboard=
                              [[newsletter],
                               [users],[orders],
                               [productAdding],[categorieAdding],
                               [bck]])

strengt_menu = InlineKeyboardMarkup(inline_keyboard=[
    [order],[back1]
])

taste_menu = InlineKeyboardMarkup(inline_keyboard=[
    [order],[back2]
])

reply_firstinfo = InlineKeyboardMarkup(inline_keyboard=[[cb],[callback1]],
resize_keyboard=True
)

reply_strenght = InlineKeyboardMarkup(
inline_keyboard=[[st1],[st2],[st3],[st4],[back]],
resize_keyboard=True
)

reply_taste = InlineKeyboardMarkup(
inline_keyboard=[[fruits],[mint],[other],[back]],
resize_keyboard=True
)

markup = InlineKeyboardMarkup(inline_keyboard=[[cb],[callback1]])

markup2 = InlineKeyboardMarkup(inline_keyboard=[[add, mybuy],
                                                [referal],
                                                [cupon]])
                               

reply_comeback = InlineKeyboardMarkup(inline_keyboard=[[buy],[bck]])

async def categories():
    all_categories = await get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(
            InlineKeyboardButton(
                text=category.name,
                callback_data=f"category_{category.id}"
            )
        )
    keyboard.add(InlineKeyboardButton(text='🔙 Назад', callback_data="main_menu"))
    return keyboard.adjust(2).as_markup()

async def categorie(category_id):
    all_categories = await get_categories2(category_id)
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(
            InlineKeyboardButton(
                text=category.name,
                callback_data=f"category2_{category.id}"  # <-- исправлено
            )
        )
    keyboard.add(InlineKeyboardButton(text='🔙 Назад', callback_data="main_menu"))  # <-- исправлено
    return keyboard.adjust(2).as_markup()

async def products(category2_id):
    all_categories = await get_category_item(category2_id)
    keyboard = InlineKeyboardBuilder()
    for product in all_categories:
        keyboard.add(
            InlineKeyboardButton(
                text=product.name,
                callback_data=f"product_{product.id}"
            )
        )
    keyboard.add(InlineKeyboardButton(text='🔙 Назад', callback_data="main_menu"))
    return keyboard.adjust(2).as_markup()