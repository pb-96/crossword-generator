from fastapi import FastAPI
from .custom_schedular.schedule import repeat_every_day
from .cw_gen.generate import generate_cw

app = FastAPI()


@repeat_every_day(hour=23, minute=0, second=0)
def generate_crossword():
    ...

