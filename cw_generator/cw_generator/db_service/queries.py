from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from schema import WordVectorStore, CWGeneric
from datetime import datetime, timedelta
from cw_generator.custom_types import Config


def get_session(db_engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


def get_random_shuffle(session, config_dict: Config, chunk: int, page: int = 1):
    if page < 0:
        page = 1

    delta = datetime.datetime.utcnow() - timedelta(
        weeks=config_dict["look_back_weeks"], days=config_dict["look_back_days"]
    )

    offset = (page - 1) * chunk
    query = (
        session.query(WordVectorStore)
        .filter(
            (WordVectorStore.last_used == None) | (WordVectorStore.last_used > delta)
        )
        .order_by(func.random())
    )

    rows = query.limit(chunk).offset(offset).all()

    for row in rows:
        row.last_used = func.now()

    session.commit()
    return rows


def get_today_crossword(client_timestamp: datetime) -> CWGeneric:
    return
