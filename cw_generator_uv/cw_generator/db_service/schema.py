from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.types import LargeBinary, DateTime, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.dialects.postgresql import ARRAY
import datetime


class WordsByLocation(DeclarativeBase):
    related_uuid = (
        Column("uuid", Integer, ForeignKey("CWGeneric.uuid"), nullable=False),
    )
    word = Column(String)
    # Demensions set to 2 to represent (int, int)
    location_tuple_start = Column(ARRAY(Integer), as_tuple=True, demensions=2)
    location_tuple_end = Column(ARRAY(Integer), as_tuple=True, demensions=2)
    description = Column(String)


class CWGeneric(DeclarativeBase):
    __tablename__ = "cw_generic"
    uuid = Column(UUID(as_uuid=True))
    generated_on = Column(DateTime(timezone=True), default=datetime.datetime.timestamp)
    cw_bytes = Column(LargeBinary)
    encoding_func: Mapped[str] = Column(String(128))


class WordVectorStore(DeclarativeBase):
    __tablename__ = "word_vector_store"
    word: Mapped[str] = Column(String(128 * 4))
    description: Mapped[str] = Column(String(256 * 4), default=None)
    embedding: Mapped[str] = Column(LargeBinary, nullable=True)
    # None here would be it was never used
    last_used = Column(DateTime(timezone=True), default=None)
