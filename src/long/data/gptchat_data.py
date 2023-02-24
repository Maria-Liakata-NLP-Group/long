from long.data.source import AggregateSource
import pandas as pd
from icecream import ic
from pathlib import Path

_generate_chat_text_dir = (
    Path(__file__).parent / ".." / ".." / ".." / "generate_chat_text"
)
generate_chat_text_dir = _generate_chat_text_dir.resolve()

"""


Contents of the `generate_chat_text_dir` dir:

"individual_thread_{thread_id}.csv"     | An individual output from ChatGPT for a single prompt. Note that this are
                                          not guaranteed to be well formed. There are lots of formatting mistakes and
                                          they do not parse cleanly using most CSV parsers.
"combined_raw_threads_{now_str}.json"   | The combination of multiple individual_thread_* files. Still not guaranteed
                                          to be well formed.
"normalised_thread_pool.json"           | The raw data, converted into teh first normative form. Each row represents a
                                          single message within a thread.
"main_collection.json"                  | The data, resampled to create a larger example dataset, by applying different
                                          date and users to randomly selected threads.

"""


def aggregate_by_user(full_df: pd.DataFrame):
    full_df["date"] = full_df["timestamp"].apply(lambda ts: ts.date())
    group_by_user = (
        full_df[["username", "date", "msg_id"]]
        .groupby(["username", "date"], as_index=False)
        .count()
    )
    group_by_user.columns = ["username", "date", "posts"]  # inplace=True)
    # ic(group_by_user.describe())
    ic(group_by_user.head(20))

    data_daily_interactions = {}

    for user_id in group_by_user["username"].unique():
        user_full_tl = group_by_user[group_by_user["username"] == user_id].copy()
        data_daily_interactions[user_id] = user_full_tl

    return data_daily_interactions


def aggregate_by_thread(full_df: pd.DataFrame):
    full_df["date"] = full_df["timestamp"].apply(lambda ts: ts.date())
    group_by_user = (
        full_df[["thread_id", "date", "msg_id"]]
        .groupby(["thread_id", "date"], as_index=False)
        .count()
    )
    group_by_user.columns = ["thread_id", "date", "posts"]  # inplace=True)
    # ic(group_by_user.describe())
    ic(group_by_user.head(20))

    data_daily_interactions = {}

    for user_id in group_by_user["thread_id"].unique():
        user_full_tl = group_by_user[group_by_user["thread_id"] == user_id].copy()
        data_daily_interactions[user_id] = user_full_tl

    return data_daily_interactions


def prep_gptchat_by_thread_source():
    main_collection = pd.read_json(generate_chat_text_dir / "main_collection.json")
    daily_interactions = aggregate_by_user(main_collection)
    cmocs = {}
    _source = AggregateSource("gptchat_by_thread", daily_interactions, cmocs)
    _source.full_timeline_df = main_collection

    return _source


def prep_gptchat_by_user_source():
    main_collection = pd.read_json(generate_chat_text_dir / "main_collection.json")
    daily_interactions = aggregate_by_user(main_collection)
    cmocs = {}
    _source = AggregateSource("gptchat_by_user", daily_interactions, cmocs)
    _source.full_timeline_df = main_collection

    return _source


gptchat_by_user_source = prep_gptchat_by_user_source()
gptchat_by_thread_source = prep_gptchat_by_thread_source()
