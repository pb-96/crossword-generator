import requests
from pathlib import Path

URL = "https://raw.githubusercontent.com/matthewreagan/WebstersEnglishDictionary/refs/heads/master/dictionary_alpha_arrays.json"


def get_raw_data(url: str):
    data_fetched = requests.get(url)
    return data_fetched.json


def write_to_file(path: Path): ...


if __name__ == "__main__":
    # Method here is to download and dump

    data = get_raw_data(URL)
    print("Data Got")
