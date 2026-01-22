import requests
from typing import List, Dict, Callable
from schema import WordVectorStore
from sqlalchemy import Engine
from cw_generator.db_service.queries import get_session
from functools import partial
import logging


URL = "https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/refs/heads/master/dictionary_alpha_arrays.json"

def get_raw_data(url: str) -> List[Dict[str, str]]:
    data_fetched = requests.get(url)
    return data_fetched.json()


def normalize_data(fetch_data_fn: Callable[[], List[Dict[str, str]]]):
    # Don't specify the parameters use functools partial before invoking the function
    all_data = fetch_data_fn()
    for idx in range(27):
        current_letter_list = all_data[idx]
        for word, description in current_letter_list.items():
            yield WordVectorStore(word=word, description=description)

def write_to_database(db_engine: Engine): 
    try:
        fn_data = partial(get_raw_data, url=URL)
        with get_session(db_engine) as session:
            for word_vector_store in normalize_data(fn_data):
                session.add(word_vector_store)
            session.commit()
    except Exception as e:
        logging.error(f"Error writing to database: {e}")
        return False
    return True
