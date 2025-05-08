from app.database.models import async_session
from datetime import datetime
from app.database.models import User, Category, Product, Category2, Bonus, Purchase


from sqlalchemy import select, update
from sqlalchemy import delete as sa_delete


async def set_user(tg_id: int, name: str, username: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id,
                             name=name,
                             userName=username))
            await session.commit()
            return True  # пользователь был добавлен
        return False  # пользователь уже есть
    
    
    
    
async def chekAdmin(tg_id: int):
    async with async_session() as session:
        chek = await session.scalar(select(User.admintag).where(User.tg_id == tg_id))
        
        if chek == 1:
            return True
        else:
            return False
    
    
async def get_all_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()  # вернёт список строк
    
async def new_item(name: str, strenght: int, taste: str, description: str, price: int, quantity: int, category: int):
    async with async_session() as session:
        new_item = Product(
            name = name,
            strenght=strenght,
            taste=taste,
            description=description,
            price=price,
            quantity=quantity,
            category=category
        )
        session.add(new_item)
        await session.commit()
        
async def additem_toAll(name: str, strenght: int, taste: str, description: str, price: int, quantity: int):
    async with async_session() as session:
        new_item = Product(
            name = name,
            strenght=strenght,
            taste=taste,
            description=description,
            price=price,
            quantity=quantity,
            category=7
        )
        session.add(new_item)
        await session.commit()
        
async def userInfo(tg_id: int):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))
        
async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))
    
async def get_categories2(category_id):
    async with async_session() as session:
        return await session.scalars(select(Category2).where(Category2.category == category_id))
    
async def get_category_item(category_id):
    async with async_session() as session:
        return await session.scalars(select(Product).where(Product.category == category_id))
    
async def get_item(item_id):
    async with async_session() as session:
        return await session.scalar(select(Product).where(Product.id == item_id))
    
async def broadcast_users():
    async with async_session() as session:
        result = await session.execute(select(User.tg_id))
        return [row[0] for row in result.fetchall()]

async def new_bonus(name: str, reward: int):
    async with async_session() as session:
        chek = await session.scalar(select(Bonus).where(Bonus.name == name))

        if not chek:
            session.add(Bonus(name=name,
                             reward=reward))
            await session.commit()
            return True  # пользователь был добавлен
        return False  # пользователь уже есть

async def set_bonuce(text: str, user: int):
    async with async_session() as session:
        bonus = await session.scalar(select(Bonus).where(Bonus.name == text))
        chek = await session.scalar(select(Bonus.reward).where(Bonus.name == text))
        userBonus = await session.scalar(select(User.bonuce).where(User.tg_id == user))
        user = await session.scalar(select(User).where(User.tg_id == user))
        
        
        if not chek or bonus.activations == bonus.availableActivations:
            return False
        
        add = chek + userBonus
        user.bonuce = add
        bonus.activations = bonus.activations + 1
        
        await session.commit()
        return True
    
async def userbuy(tg_id):
    async with async_session() as session:
        result = await session.execute(select(Purchase).where(Purchase.tg_id == tg_id))
        if not result:
            return False
        return result.scalars().all()  # вернёт список строк
        return True
    