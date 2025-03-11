from fastapi import FastAPI
from .custom_schedular.schedule import repeat_every_day
from .cw_gen.generate import generate_cw
from sqlalchemy import create_engine


db = create_engine("sqlite://", echo=True)

app = FastAPI()


@repeat_every_day(hour=23, minute=0, second=0)
def generate_crossword(): ...


app.route("get-current-cw/{client-timestamp}")


def get_current_cw(client_timestamp: str):
    # Convert client timestamp to datetime object

    ...
