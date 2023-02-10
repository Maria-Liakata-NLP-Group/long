from long.data.utils.gptchat_resampler import resample, AllUserPool, get_time_delta
from long.data.gptchat_data import aggregate_by_user
import pytest
from icecream import ic
import pandas as pd
from pathlib import Path
import math


def test_resample():
    threads = 2
    users = 50
    df = resample(threads, users)

    assert len(df["thread_id"].unique()) == threads
    assert len(df["username"].unique()) <= users


def test_all_user_pool():
    pool_size = 10
    aup = AllUserPool(pool_size)
    actual = set(aup.get_user_selection(pool_size))
    # Given that we are requesting the same number of users as exist in the pool, then we should expect exactly one of each
    expected = set([f"gptchat_user_{n}" for n in range(pool_size)])

    assert actual == expected

    with pytest.raises(ValueError):
        ic(aup.get_user_selection(pool_size + 1))


def test_get_time_delta():
    test_size = 10000
    # Units in seconds
    time_deltas = [get_time_delta() for _ in range(test_size)]
    stats = pd.DataFrame(time_deltas).describe().to_dict()[0]
    ic(stats)
    assert stats["count"] == test_size
    assert stats["max"] < 240 * 3600
    assert stats["min"] > 36


def test_generate_chat_text_dir():
    from long.data.gptchat_data import generate_chat_text_dir

    assert generate_chat_text_dir.exists()
    assert generate_chat_text_dir.is_dir()
