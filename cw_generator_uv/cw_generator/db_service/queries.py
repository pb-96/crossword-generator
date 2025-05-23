from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import func, and_
from schema import WordVectorStore, CWGeneric, WordsByLocation
from datetime import datetime, timedelta
from cw_generator.custom_types import Config
from fastapi_sqlalchemy import db
from typing import cast, Union, Dict, Tuple, List
from cw_generator.utils import decompress, compress
from cw_generator.custom_types import CWPoint
from cw_generator.custom_types import (
    MATRIX_TYPE,
    SupportedCompression,
    WordByLocationDict,
)
from uuid import uuid4, UUID


def get_session(db_engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


def get_random_shuffle(config_dict: Config, page: int = 1):
    with db(commit_on_exit=True):
        session = db.session
        if page < 0:
            page = 1

        delta = datetime.now() - timedelta(
            weeks=config_dict["look_back_weeks"], days=config_dict["look_back_days"]
        )
        chunk = config_dict["default_chunk"]
        offset = page * chunk
        query = (
            session.query(WordVectorStore)
            .filter(
                (WordVectorStore.last_used == None)
                | (WordVectorStore.last_used > delta)
            )
            .order_by(func.random())
        )

        rows = query.limit(chunk).offset(offset).all()

        for row in rows:
            row.last_used = func.now()

        session.commit()
        return rows


def get_today_crossword(client_timestamp: Union[datetime, None]) -> CWPoint:
    with db():
        session = cast(Session, db.session)
        if client_timestamp is None:
            client_timestamp = datetime.now()

        today = datetime.date()
        # forward back comparison
        forward = today + timedelta(days=1)
        backward = today + timedelta(days=-1)

        query = session.query(CWGeneric).filter(
            and_(CWGeneric.generated_on < forward, CWGeneric.generated_on > backward)
        )
        result: CWGeneric = query.first()

        decompressed_matrix = decompress(result.cw_bytes, result.encoding_func)
        related_words = (
            session.query(WordsByLocation)
            .filter(WordsByLocation.related_uuid == result.uuid)
            .all()
        )
        words_and_descriptions: Dict[str, str] = {}
        words_and_locations: Dict[str, Tuple[int, int]] = {}

        for row in related_words:
            words_and_descriptions[row.word] = row.description
            words_and_locations[row.word] = (
                row.location_tuple_start,
                row.location_tuple_end,
            )

        return_type = CWPoint(
            words_description=words_and_descriptions,
            words_locations=words_and_locations,
            cw_matrix=decompressed_matrix,
        )

        return return_type


def create_cross_word_entry(
    cw_matrix: MATRIX_TYPE,
    words: Union[List[WordByLocationDict], List[WordVectorStore]],
    cw_uuid: Union[str, UUID] = None,
    compress_func: SupportedCompression = SupportedCompression.base64,
):
    if cw_uuid is None:
        cw_uuid = str(uuid4())
    elif isinstance(cw_uuid, UUID):
        cw_uuid = str(cw_uuid)

    compressed_matrix = compress(cw_matrix, compress_func)
    try:
        with db():
            session = cast(Session, db.session)
            if isinstance(words[0], WordByLocationDict):
                words_by_location = []
                for element in words:
                    obj = WordsByLocation(
                        related_uuid=cw_uuid,
                        word=element["word"],
                        description=element["description"],
                        location_tuple_start=element["location_tuple_start"],
                        location_tuple_end=element["location_tuple_end"],
                    )
                    words_by_location.append(obj)
                session.add_all(words_by_location)
            else:
                session.add_all(words)

            session.add(
                CWGeneric(
                    uuid=cw_matrix,
                    cw_bytes=compressed_matrix,
                    encoding_func=compress_func.value,
                )
            )

            session.commit()

    except Exception as e:
        return False

    return True
