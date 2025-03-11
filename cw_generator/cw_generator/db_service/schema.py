from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, Column
from sqlalchemy.types import Datetime, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship
import datetime


class Base(DeclarativeBase):
    pass


class CWGeneric(Base):
    __tablename__ = "cw_generic"
    generated_on = Column(DateTime(timezone=True), default=datetime.datetime.timestamp)
    cw_bytes = Column(LargeBinary)
    encoding_func: Mapped[str] = Column(String(128))


class WordVectorStore(Base):
    __tablename__ = "word_vector_store"
    word: Mapped[str] = Column(String(128 * 4))
    description: Mapped[str] = Column(String(256 * 4))
    embedding: Mapped[str] = Column(LargeBinary)
