from fastapi import FastAPI
from .custom_schedular.schedule import repeat_every_day
from .cw_gen.generate import generate_cw
from sqlalchemy import create_engine
from custom_types import CWPoint, Config, ReplaceStrategy
from typing import Union
import Dynaconf


settings = Dynaconf(settings_files=["settings.toml"], envvar_prefix="DYNACONF")
engine = create_engine(settings.DATABASE_URL)
app = FastAPI()

CONFIG_DICT: Config = {
    # How many words you want by default
    "default_chunk": 15,
    "sort_strategy": ReplaceStrategy.sort_lr,
    "look_back_days": 0,
    "look_back_weeks": 1
}

@repeat_every_day(hour=23, minute=0, second=0)
def generate_crossword() -> True:
    # Query words
    # Will need a shuffle query
    # Run words through a cross word generator

    return True


@app.get("get-current-cw/{client-timestamp}")
def get_current_cw(client_timestamp: Union[str, None]) -> CWPoint:
    # Convert client timestamp to datetime object

    ...
