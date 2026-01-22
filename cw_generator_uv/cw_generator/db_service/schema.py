from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.types import LargeBinary, DateTime, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY
import datetime
from typing import Optional, Tuple


class WordsByLocation(DeclarativeBase):
    related_uuid = Column("uuid", Integer, ForeignKey("CWGeneric.uuid"), nullable=False)
    word = Column(String)
    # Demensions set to 2 to represent (int, int)
    location_tuple_start: Mapped[Tuple[int, int]] = mapped_column(ARRAY(Integer), as_tuple=True, demensions=2)
    location_tuple_end: Mapped[Tuple[int, int]] = mapped_column(ARRAY(Integer), as_tuple=True, demensions=2)
    description = Column(String)


class CWGeneric(DeclarativeBase):
    __tablename__ = "cw_generic"
    uuid = Column(UUID(as_uuid=True))
    generated_on = Column(DateTime(timezone=True), default=datetime.datetime.timestamp)
    cw_bytes: Mapped[bytes] = mapped_column(LargeBinary)
    encoding_func: Mapped[str] = mapped_column(String(128))


class WordVectorStore(DeclarativeBase):
    __tablename__ = "word_vector_store"
    word: Mapped[str] = mapped_column(String(128 * 4))
    description: Mapped[Optional[str]] = mapped_column(String(256 * 4), default=None)
    embedding: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    # None here would be it was never used
    last_used: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), default=None)


class User(DeclarativeBase):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(128), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now)
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.now)