from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, Column, Integer
from sqlalchemy.types import Datetime, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.dialects.postgresql import ARRAY
import datetime


class CWGeneric(DeclarativeBase):
    __tablename__ = "cw_generic"
    generated_on = Column(DateTime(timezone=True), default=datetime.datetime.timestamp)
    cw_bytes = Column(LargeBinary)
    encoding_func: Mapped[str] = Column(String(128))
    # words: List[ForeignKey] = relationship("WordVectorStore", uselist=True)
    words: Mapped[str] = Column(ARRAY(String))
    words_by_locations = Column(ARRAY(Integer), as_tuple=True)


class WordVectorStore(DeclarativeBase):
    __tablename__ = "word_vector_store"
    word: Mapped[str] = Column(String(128 * 4))
    description: Mapped[str] = Column(String(256 * 4), default=None)
    embedding: Mapped[str] = Column(LargeBinary)
    # None here would be it was never used
    last_used = Column(Datetime(timezone=True), default=None)
