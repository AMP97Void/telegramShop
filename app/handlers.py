from aiogram import F, Router
from aiogram.types import Message 
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, CallbackQuery
import sqlite3
import app.keyboard as kb 
import app.database.request as rq

router = Router()


# КОМАНДЫ COMMANDS

@router.message(CommandStart())
async def start(message: Message):
    
    
    
    usName = message.from_user.first_name
    usId = message.from_user.id
    us = message.from_user.username
    
    replenishemt = '0'
    usPseudonim = ' '
    tag = ' '
    
    bonuce = 0
    balance = 0
    
    # tg_id: int, name: str, userId: str, data: datetime, money: int, bonuce: int, username: str
    
    reg = await rq.set_user(tg_id = message.from_user.id,
                      name = message.from_user.first_name,
                      username = message.from_user.username
                      )
    
    if reg:
        await message.answer('💭Хотите получить основную информацию?', reply_markup=kb.markup)
    
    user_id = message.from_user.id
    chekadmin = await rq.chekAdmin(tg_id = user_id)
    if chekadmin:
        await message.answer(f'✨Добро пожаловать, {message.from_user.first_name}!\n\n🔸Бот готов к использованию.\n'
                             '🔸Вы вошли в режим админа бота\n'
                             '🔸Если не появилось вспомогательные кнопки\n'
                             '🔸Введите /start'
                             '🔸Чтобы узнать все возможности пользования ботом используй /ahelp\n'
                             '🔸Все действия в этом режиме логируются!'
                             '🌐 Разработчик - @A006MP\\_97\n\n'
                             '🔸Основной Телеграмм канал: [Перейти](https://t.me/+6LOgd170w04xZWVi)'
                             '[💭Отзывы Покупателей](https://t.me/+gYkK90TrceQ3MDli)', parse_mode='Markdown', disable_web_page_preview=True,
                             reply_markup=kb.reply_apanel)
    else:
        await message.answer(f'✨Добро пожаловать, {message.from_user.first_name}!\n\n'
                             '🔸Бот готов к использованию.\n'
                             '🔸Если не появилось вспомогательные кнопки\n'
                             '🔸Введите /start\n🔸Посмотреть основные команды: /help\n'
                             '🔸Основной Телеграмм канал: [Перейти](https://t.me/+6LOgd170w04xZWVi)'
                             '\n🌐 Разработчик - @A006MP\\_97\n\n'
                             '[💭Отзывы Покупателей](https://t.me/+gYkK90TrceQ3MDli)', parse_mode='Markdown', disable_web_page_preview=True, 
                             reply_markup=kb.user_keyboard)
    
@router.callback_query(F.data.startswith('category_'))
async def categorz(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    await callback.answer()
    await callback.message.answer(
        'Вы выбрали категорию!\nВыберите подкатегорию:',
        reply_markup=await kb.categorie(category_id)
    )

@router.callback_query(F.data.startswith('category2_'))
async def category(callback: CallbackQuery):
    category2_id = int(callback.data.split('_')[1])
    await callback.answer()
    await callback.message.answer(
        'Вы выбрали подкатегорию!\nВыберите товар:',
        reply_markup=await kb.products(category2_id)
    )

@router.callback_query(F.data.startswith('product_'))
async def product_info(callback: CallbackQuery):
    item_id = int(callback.data.split('_')[1])
    item_data = await rq.get_item(item_id)
    await callback.answer('Вы выбрали товар')
    await callback.message.answer(
        f'Информация о товаре:\n'
        f'➖➖➖➖➖➖➖➖➖➖➖\n'
        f'🏷 Название: *{item_data.name}*\n\n'
        f'🍓 Вкус: {item_data.taste}\n'
        f'💪 Крепкость: {item_data.strenght}\n'
        f'💰 *Стоимость: {item_data.price}*\n'
        f'📦 Количество: {item_data.quantity}\n'
        f'📜 Описание: {item_data.description}\n\n'
        'По всем вопросам обращайтесь к [Админу](https://t.me/A006MP_97)\n\n'
        '[💭Отзывы Покупателей](https://t.me/+gYkK90TrceQ3MDli)',
        parse_mode='Markdown',
        disable_web_page_preview=True, reply_markup=kb.reply_comeback
    )
    
    
@router.callback_query(F.data == 'go_back')
async def menu(callback: CallbackQuery):
    await callback.message.delete()

@router.message(Command("help"))
async def menu(message: Message):
    await message.answer('Основные команды для управления ботом:\n\n    ✅ /start - Перезапустить бота\n    ❓ /help - Открыть меню помощи\n    ⚙️ /ahelp - Панель Администратора \n    🛠 /support  - Тех. поддержка бота\n    🔍 /search - Поиск товара по названию\n    📩 /send - Отправить сообщение Администратору')
    
@router.message(Command('list'))
async def listmenu(message: Message):
    photo = FSInputFile(r"C:\Users\dmitr\Desktop\Aiogramm\photos\listPhoto.jpg")
    await message.answer_photo(photo)
    await message.answer("Выберите категорию товара!", reply_markup = kb.reply_categories)
# КOЛЛБЕКИ CALLBACK

@router.message(Command("support"))
async def support(message: Message):
    photoSup = FSInputFile(r"C:\Users\dmitr\Desktop\Aiogramm\photos\adminPhoto.jpg")
    await message.answer_photo(photoSup,'*Технический раздел бота:\n\n*'
                     '👥 *Контакты:*'
                     '\n🧖🏻 [Тех. Администратор](https://t.me/A006MP_97)'
                     '\n\n_Если вы нашли какую-то ошибку или бот работает не корректо просьба сообщить об этом!_'
                     '\n_Версия бота_ *1.0*', parse_mode = 'Markdown') 
    
    
    
# КНОПКИ BUTTONS

@router.message()
async def reply_to_buttons(message: Message):
    if message.text == "💳 Заказать":
        await message.answer("Кнопка *заказать* была нажата", parse_mode = 'markdown')
    elif message.text == "ℹ️ Помощь":
        photoHelp = FSInputFile(r"C:\Users\dmitr\Desktop\Aiogramm\photos\rulesPhoto.jpg")
        await message.answer_photo(photoHelp,'👥*Контакты:*'
                     '\n 🧖🏻[Администратор](https://t.me/A006MP_97)'
                     '\n\n📢*Ссылки:*'
                     '\n 🔥[Канал магазина](https://t.me/+6LOgd170w04xZWVi)'
                     '\n 🔥[Отзывы](https://t.me/+gYkK90TrceQ3MDli)'
                     '\n\n❗️ *Правила:*'
                     '\n\n*1.*Пользователь согласен, что время обработки заявки занимает до 1 рабочего дня.'
                     '\n\n*1.1* Флуд, мат, оскорбления, невежливое общение, введение в заблуждение, обман - причины ограничения поддержки/доступа к боту без дальнейшей помощи в разбирательстве вашей проблемы.'
                     '\n\n*1.2* Купленный и позже вскрытый вами товар не подлежит возврату! Если Вы купили товар, но после покупки захотели поменять вкус, не открыв упаковку мы поможем вам решить эту проблему.'
                     '\n\n *1.3* Оплата товара происходит только наличными средствами и только при личной встречи. Перед покупкой товара нельзя попробовать его.'
                     '\n\n *1.4* За любые попытки сломать бота или черезмерную активность в заказах - будет ограничен доступ, как к поддержке, так и к доступу бота.'
                     '\n\n *1.5* Места встреч фиксированы и у нас нету такой функции, как доставка. Так что просьба не писать с просьбами привезти товар к вашему дома и тд.'
                     '\n',parse_mode = 'markdown')
    elif message.text == "📃 Список":
        photo = FSInputFile(r"C:\Users\dmitr\Desktop\Aiogramm\photos\listPhoto.jpg")
        await message.answer_photo(photo)
        await message.answer('Выберите категорию товара', reply_markup=await kb.categories())
        
    elif message.text == "💻 Админ Панель":
        user_id = message.from_user.id
        chekadmin = await rq.chekAdmin(tg_id = user_id)
        if chekadmin:
            await message.answer("Вы вошли в Админ панель!", reply_markup=kb.apanel)
        else:
            await message.answer("Эта команда вам не доступна...")

# КOЛЛБЕКИ CALLBACK

@router.callback_query(F.data == "call")
async def firstInfo(callback: CallbackQuery):
    await callback.message.edit_text('<b>      Основная информация:</b>'
                                      '\n<i> Для упрощения работы нашего магазина, мы создали этого телеграмм бота! '
                                      'Здесь Вы сможете найти весь товар, посмотреть его наличия, а также быстро и удобно сделать предзаказ. '
                                      'После предзаказа с вами свяжется менеджер нашего магазина и договорится с вами о встрече! '
                                      'Если у вас возникли какие-то вопросы или же проблемы с работой нашего бота, просим сообщить об этом нам!'
                                      ' Для связи с нами, вы можете написать нам в личные сообщение или же сделать это прямо в боте, использоваав команду - </i>'
                                      '/send'
                                      '\n<i> Для просмотра всех команд используйте -</i> /help'
                                      '\n\n\n<b>     График выдачи товара:</b>'
                                      '\n\n 🕐Будние дни с 16:00 до 21:00'
                                      '\n 🕐Выходные, праздники с 12:00 до 23:00'
                                      '\n\n<b>     Места для встречи:</b>'
                                      '\n\n 📍Berlin Zoologischer Garten'
                                      '\n 📍Potsdamer Platz'
                                      '\n 📍Brandenburger Tor'
                                      '\n 📍Friedrichstraße'
                                      '\n 📍Hackesher Markt'
                                      '\n 📍Alexanderplatz',parse_mode='HTML')
    await callback.answer()
    
@router.callback_query(F.data == "call2")
async def firstInfo(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

        
        
@router.callback_query(F.data == "alle")
async def all_products(callback: CallbackQuery):
    await callback.message.edit_text('<b>Вот список всех доступных товаров:</b> \n\n'
                              ' <b>     Killa Edition: </b>'
                              '\n🍏 Killa Apple <i>(16,8MG Цена: 7)</i> '
                              '\n🍉 Killa Watermelon <i>(16,8MG Цена: 7)</i>'
                              '\n🥃 Killa Cola <i>(16,8MG Цена: 7)</i>'
                              '\n❄️ Killa Frosted Mint <i>(30MG Цена: 7)</i>'
                              '\n\n<b>     Pablo Exclusive Edition: </b>'
                              '\n🍌 Pablo Banane <i>(30MG Цена: 7.50)</i> '
                              '\n🥝 Pablo Exclusive Kiwi <i>(30MG Цена: 7.50)</i>'
                              '\n🥭 Pablo Exclusive Mango Ice <i>(30MG Цена: 7.50)</i>'
                              '\n\n<b>     Zeus Edition: </b>'
                              '\n🫐 Zeus Epic Berry <i>(50MG Цена: 7.50)</i> '
                              '\n🍃 Zeus Tropic <i>(50MG Цена: 7.50)</i> '
                              '\n🍋 Zeus Zitrone <i>(50MG Цена: 7.50)</i> '
                              '\n\n<b>     Nois Edition: </b>'
                              '\n🥭 Nois Mango <i>(60MG Цена: 7.50)</i>'
                              '\n❄️ Nois Mint  <i>(60MG Цена: 7.50)</i>'
                              '\n🍇 Nois Grape ice <i>(60MG Цена: 7.50)</i>'
                              '\n🫐 Nois Blueberry <i>(60MG Цена: 7.50)</i>'
                              '\n\n<b>     Pablo Edition: </b>'
                              '\n❄️ Pablo Ice Cold <i>(75MG Цена: 7.50)</i>'
                              '\n\n <b>     Cuba black Edition: </b>'
                              '\n🍒 Cuba Cherry <i>(160MG Цена: 8.50)</i>'
                              '\n🥃 Cuba Cola  <i>(160MG Цена: 8.50)</i>'
                              '\n🍑 Cuba Peach <i>(160MG Цена: 8.50)</i>'
                              '\n\n<b>     Iceberg Edition: </b>'
                              '\n❄️ Iceberg Menthol <i>(160MG Цена: 8.50)</i>', parse_mode='HTML', reply_markup = kb.main_menu)
    await callback.answer()
    
    
    
    
@router.callback_query(F.data == "strenght")
async def open_strenght(callback: CallbackQuery):
    await callback.message.edit_text('Выберите категорию товара!', reply_markup= kb.reply_strenght)
    await callback.answer()
    
@router.callback_query(F.data == "low")
async def low_strenght(callback: CallbackQuery):
    await callback.message.edit_text( "<b>Вот список всех доступных товаров:</b> \n\n <b>  Curwa Collection:</b>\n🥭 Снюс Kurwa Collection Mango Raspberry <i>(16,8MG Цена: 6.50)</i>\n🍓 Снюс Kurwa Collection Raspberry Strawberry  <i>(16,8MG Цена: 6.50)</i>\n👄 Снюс Kurwa Collection Strawberry Gym <i>(16,8MG Цена: 6.50)</i> \n\n <b>  Velo Edition:</b>\n❄️ Velo Mint <i>(14MG Цена: 6.50)</i>\n🍒 Velo Icy Cherry <i>(14MG Цена: 6.50)</i>",parse_mode='HTML', reply_markup = kb.strengt_menu)
    await callback.answer()

@router.callback_query(F.data == "medium")
async def medium_strenght(callback: CallbackQuery):
    await callback.message.edit_text('<b>Вот список всех доступных товаров:</b> \n\n'
                              ' <b>     Killa Edition: </b>'
                              '\n🍏 Killa Apple <i>(16,8MG Цена: 7)</i> '
                              '\n🍉 Killa Watermelon <i>(16,8MG Цена: 7)</i>'
                              '\n🥃 Killa Cola <i>(16,8MG Цена: 7)</i>'
                              '\n❄️ Killa Frosted Mint <i>(30MG Цена: 7)</i>'
                              '\n\n<b>     Pablo Exclusive Edition: </b>'
                              '\n🍌 Pablo Banane <i>(30MG Цена: 7.50)</i> '
                              '\n🥝 Pablo Exclusive Kiwi <i>(30MG Цена: 7.50)</i>'
                              '\n🥭 Pablo Exclusive Mango Ice <i>(30MG Цена: 7.50)</i>'
                              '\n\n<b>     Zeus Edition: </b>'
                              '\n🫐 Zeus Epic Berry <i>(50MG Цена: 7.50)</i> '
                              '\n🍃 Zeus Tropic <i>(50MG Цена: 7.50)</i> '
                              '\n🍋 Zeus Zitrone <i>(50MG Цена: 7.50)</i> '
                              '\n🥭 Nois Mango <i>(60MG Цена: 7.50)</i>'
                              ,parse_mode = 'HTML', reply_markup = kb.strengt_menu)
    await callback.answer()

@router.callback_query(F.data == "high")
async def high_strenght(callback: CallbackQuery):
    await callback.message.edit_text('<b>Вот список всех доступных товаров:</b> \n\n'
                             ' <b>     Nois Edition: </b>'
                             '\n🥭 Nois Mango <i>(60MG Цена: 7.50)</i>'
                             '\n❄️ Nois Mint  <i>(60MG Цена: 7.50)</i>'
                             '\n🍇 Nois Grape ice <i>(60MG Цена: 7.50)</i>'
                             '\n🫐 Nois Blueberry <i>(60MG Цена: 7.50</i>'
                             '\n\n<b>     Pablo Edition: </b>'
                             '\n❄️ Pablo Ice Cold <i>(75MG Цена: 7.50)</i>',parse_mode = 'HTML', reply_markup = kb.strengt_menu)
    await callback.answer()

@router.callback_query(F.data == "extra")
async def extra_strenght(callback: CallbackQuery):
    await callback.message.edit_text(' <b>     Cuba black Edition: </b>'
                             '\n🍒 Cuba Cherry <i>(160MG Цена: 8.50)</i>'
                             '\n🥃 Cuba Cola  <i>(160MG Цена: 8.50)</i>'
                             '\n🍑 Cuba Peach <i>(160MG Цена: 8.50)</i>'
                             '\n\n<b>     Iceberg Edition: </b>'
                             '\n❄️ Iceberg Menthol <i>(160MG Цена: 8.50)</i>',parse_mode = 'HTML', reply_markup = kb.strengt_menu)
    await callback.answer()
    
@router.callback_query(F.data == "usersList")
async def userList(callback: CallbackQuery):
    user_id = callback.from_user.id
    chekadmin = await rq.chekAdmin(tg_id = user_id)
    if chekadmin:
        
        users = await rq.get_all_users()

        if not users:
            await callback.message.answer("Пользователей пока нет.")
            return

        text = "👤 Список пользователей:\n\n"
        for user in users:
            name = user.name or "Без имени"
            username = f"@{user.userName}" if user.userName else "нет username" 
            dataReg = user.data
            text += f"• {name} | {username} | userID: <code>{user.tg_id}</code>\n Деньги: <pre>{user.money}</pre> | Бонусы: <pre> {user.bonuce}</pre> | Время рег-ии: <pre>{dataReg}</pre>\n\n"

        await callback.message.answer(text, parse_mode='html')
    
@router.callback_query(F.data == "taste")
async def taste_menu(callback: CallbackQuery):
    await callback.message.edit_text('Выберите категорию товара!',reply_markup = kb.reply_taste)
    await callback.answer()

@router.callback_query(F.data == "fruit")
async def fuits_taste(callback: CallbackQuery):
    await callback.message.edit_text('<b>Вот список всех доступных товаров:</b> \n\n'
                            '\n🥭 Снюс Kurwa Collection Mango Raspberry <i>(16,8MG Цена: 6.50)</i>'
                            '\n🍓 Снюс Kurwa Collection Raspberry Strawberry  <i>(16,8MG Цена: 6.50)</i>'
                            '\n🍒 Velo Icy Cherry <i>(14MG Цена: 6.50)</i>'
                            '\n🍏 Killa Apple <i>(16,8MG Цена: 7)</i> '
                            '\n🍉 Killa Watermelon <i>(16,8MG Цена: 7)</i>'
                            '\n🍌 Pablo Banane <i>(30MG Цена: 7.50)</i> '
                            '\n🥝 Pablo Exclusive Kiwi <i>(30MG Цена: 7.50)</i>'
                            '\n🥭 Pablo Exclusive Mango Ice <i>(30MG Цена: 7.50)</i>'
                            '\n🫐 Zeus Epic Berry <i>(50MG Цена: 7.50)</i> '
                            '\n🍃 Zeus Tropic <i>(50MG Цена: 7.50)</i> '
                            '\n🍋 Zeus Zitrone <i>(50MG Цена: 7.50)</i>' ,parse_mode='HTML',reply_markup = kb.taste_menu)
    await callback.answer()

@router.callback_query(F.data == "mint")
async def mint_taste(callback: CallbackQuery):
    await callback.message.edit_text('<b>Вот список всех доступных товаров со вкусом Мята:</b> \n\n'
                             '\n❄️ Velo Mint <i>(14MG Цена: 6.50)</i>'
                             '\n❄️ Killa Frosted Mint <i>(30MG Цена: 7)</i>'
                             '\n❄️ Nois Mint  <i>(60MG Цена: 7.50)</i>'
                             '\n❄️ Pablo Ice Cold <i>(75MG Цена: 7.50)</i>'
                             '\n❄️ Iceberg Menthol <i>(160MG Цена: 8.50)</i>',parse_mode='HTML',reply_markup = kb.taste_menu)
    await callback.answer()
    
@router.callback_query(F.data == "other")
async def others_taste(callback: CallbackQuery):
    await callback.message.edit_text('<b>Вот список всех доступных товаров:</b> \n\n'
                             '\n🥃 Killa Cola <i>(16,8MG Цена: 7)</i>'
                             '\n🥃 Cuba Cola  <i>(160MG Цена: 8.50)</i>'
                             '\n👄 Снюс Kurwa Collection Strawberry Gym <i>(16,8MG Цена: 6.50)</i>',parse_mode='html',reply_markup = kb.taste_menu)
    await callback.answer()



@router.callback_query(F.data == "menu_main")
async def main_products(callback: CallbackQuery):
    await callback.message.edit_text("Выберите категорию товара!", reply_markup = kb.reply_categories)
    await callback.answer()
    
@router.callback_query(F.data == "strengt_main")
async def main_strengt(callback: CallbackQuery):
    await callback.message.edit_text("Выберите категорию товара!", reply_markup= kb.reply_strenght)
    await callback.answer()

@router.callback_query(F.data == "taste_main")
async def main_taste(callback: CallbackQuery):
    await callback.message.edit_text("Выберите категорию товара!", reply_markup= kb.reply_taste)
    await callback.answer()
    
    
@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    await callback.message.delete()
    
    