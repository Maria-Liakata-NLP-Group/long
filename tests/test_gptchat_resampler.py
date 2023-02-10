from long.data.gptchat_resampler import resample, AllUserPool, get_time_delta
from long.data.gptchat_data import aggregate_by_user
import pytest
from icecream import ic
import pandas as pd
from pathlib import Path
import math


def test_resample():
    resample(1000)

    pytest.fail()


def test_all_user_pool():
    aup = AllUserPool(10)
    ic(aup.get_user_selection(9))

    aup = AllUserPool(2)
    ic(aup.get_user_selection(2))

    pytest.fail()


def test_get_time_delta():
    time_deltas = [get_time_delta() / 3600 for _ in range(10000000)]
    df = pd.DataFrame(time_deltas)
    ic(df.describe())
    ic(math.exp(0.2))
    ic(math.log(0.2))

    pytest.fail()


def test_aggregate_main_pool():
    generate_chat_text_dir = Path(__file__).parent / ".." / "generate_chat_text"
    generate_chat_text_dir = generate_chat_text_dir.resolve()
    assert generate_chat_text_dir.exists()
    assert generate_chat_text_dir.is_dir()

    ic(generate_chat_text_dir)

    df = pd.read_json(generate_chat_text_dir / "main_collection.json")
    # ic(len(df))
    # ic(df.head())

    aggregate_by_user(df)

    pytest.fail()
