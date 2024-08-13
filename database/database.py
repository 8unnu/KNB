from datetime import datetime
from typing import Annotated

from sqlalchemy import func, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column, Mapped

from database.config import get_db_url

DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_factory = async_sessionmaker(engine, expire_on_commit=False)

# annotations
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
int_pk = Annotated[int, mapped_column(primary_key=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
score_landmark = Annotated[int, mapped_column(server_default=text('0'))]

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    created_at: Mapped[created_at]