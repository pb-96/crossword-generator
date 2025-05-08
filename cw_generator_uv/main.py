from fastapi import FastAPI
from cw_generator.custom_schedular.schedule import repeat_every_day
from cw_generator.cw_gen.generate import generate_cw
from sqlalchemy import create_engine
from cw_generator.custom_types import CWPoint, Config, ReplaceStrategy
from typing import Union
from dynaconf import Dynaconf
import datetime
from cw_generator.db_service.queries import (
    get_today_crossword,
    get_random_shuffle,
    get_session,
)
from cw_generator.utils import decompress

settings = Dynaconf(settings_files=["settings.toml"], envvar_prefix="DYNACONF")
engine = create_engine(settings.DATABASE_URL)
app = FastAPI()

CONFIG_DICT: Config = {
    # How many words you want by default
    "default_chunk": 15,
    "sort_strategy": ReplaceStrategy.sort_lr,
    "look_back_days": 0,
    "look_back_weeks": 1,
}


@repeat_every_day(hour=23, minute=0, second=0)
def generate_crossword() -> True:
    # Query words
    # Will need a shuffle query
    # Run words through a cross word generator

    return True


@app.get("get-current-cw/{client-timestamp}")
def get_current_cw(client_timestamp: Union[datetime.datetime, None]) -> CWPoint:
    session = get_session(engine)
    session.connect()
    # Convert client timestamp to datetime object
    if client_timestamp is None:
        client_timestamp = datetime.datetime.now()

    as_date_only = datetime.datetime(
        day=client_timestamp.day,
        month=client_timestamp.month,
        year=client_timestamp.year,
    )

    cw_object = get_today_crossword(as_date_only)

    try:
        decompressed_matrix = decompress(cw_object.cw_bytes, cw_object.compression_func)
    except Exception as e:
        print(str(e))

    session.disconnect()

    return CWPoint(
        words_locations=cw_object.words_by_location,
        cw_matrix=decompressed_matrix,
        words_description={},
    )
