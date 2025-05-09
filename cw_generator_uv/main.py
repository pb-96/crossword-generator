from fastapi import FastAPI
from cw_generator.custom_schedular.schedule import repeat_every_day
from cw_generator.cw_gen.generate import generate_cw
from sqlalchemy import create_engine
from cw_generator.custom_types import CWPoint, Config, ReplaceStrategy
from typing import Union, List, Dict
from dynaconf import Dynaconf
import datetime
from cw_generator.db_service.queries import get_today_crossword, get_random_shuffle
import cw_generator.db_service.schema as models
from uuid import uuid4
from cw_generator.db_service.queries import create_cross_word_entry

settings = Dynaconf(settings_files=[".settings.toml"], envvar_prefix="DYNACONF")
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
    vector_words: List[models.WordVectorStore] = get_random_shuffle()
    words_only: Dict[str, models.WordVectorStore] = {
        vc_words.word: vector_words for vc_words in vector_words
    }
    words_by_location, cw_crossword = generate_cw([*words_only.keys()])
    unique_id = str(uuid4())
    words_store = []

    for key, value in words_by_location.items():
        # Only thing missing here is the description
        description = words_only[key].description
        as_dict: models.WordsByLocation = models.WordsByLocation(
            related_uuid=unique_id,
            description=description,
            word=key,
            location_tuple_start=value["location_tuple_start"],
            location_tuple_end=value["location_tuple_end"],
        )
        words_store.append(as_dict)
    created = create_cross_word_entry(cw_matrix=cw_crossword, words=words_store)
    return created


@app.get("get-current-cw/{client_timestamp}")
def get_current_cw(client_timestamp: Union[datetime.datetime, None]) -> CWPoint:
    # Convert client timestamp to datetime object
    if client_timestamp is None:
        client_timestamp = datetime.datetime.now()
    as_date_only = datetime.datetime(
        day=client_timestamp.day,
        month=client_timestamp.month,
        year=client_timestamp.year,
    )
    cw_object = get_today_crossword(as_date_only)
    return cw_object
