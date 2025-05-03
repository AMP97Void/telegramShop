from sqlalchemy import BigInteger, Text, DateTime, String, ForeignKey, Integer
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3') # создание бд 

async_session = async_sessionmaker(engine) # Подключение к бд


class Base(AsyncAttrs, DeclarativeBase): #Основной класс, дает возможность управлять всеми дочернеми классами   
    pass

class User(Base):
    __tablename__= 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column()
    userName: Mapped[str] = mapped_column()
    bonuce: Mapped[int] = mapped_column(Integer, default=0)
    money: Mapped[int] = mapped_column(Integer, default=0)
    admintag: Mapped[int] = mapped_column(Integer, default=0)
    data: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    
class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(45))
    
class Category2(Base):
    __tablename__ = 'categories2'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(45))
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    
class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    strenght: Mapped[str] = mapped_column(Text)
    taste: Mapped[str] = mapped_column(Text)    
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    quantity: Mapped[int] = mapped_column(Integer)
    
    category: Mapped[int] = mapped_column(ForeignKey('categories2.id'))
    
    
    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)