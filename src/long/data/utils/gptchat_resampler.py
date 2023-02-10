import json
import pandas as pd
from icecream import ic
import re
import random
from io import StringIO
from csv import QUOTE_NONNUMERIC, QUOTE_ALL
import csv
import datetime
from pathlib import Path
import re
import math
from long.data.gptchat_data import generate_chat_text_dir


def create_start_time():
    # start_dt = datetime.datetime.fromisoformat("2019-01-01T00:01Z")
    earliest_dt = datetime.datetime(
        year=2019, month=1, day=1, hour=0, minute=0, second=1
    )
    latest_dt = datetime.datetime(year=2021, month=1, day=1, hour=0, minute=0, second=1)

    date_int = random.randint(int(earliest_dt.timestamp()), int(latest_dt.timestamp()))
    start_date = datetime.datetime.fromtimestamp(date_int)
    return start_date


def create_timestamps(num_posts: int):
    start = create_start_time()
    result = [start]
    last_time = start.timestamp()

    for _ in range(1, num_posts):
        last_time = last_time + get_time_delta()
        result.append(datetime.datetime.fromtimestamp(last_time))

    return result


def get_time_delta():
    """
    Number of seconds between posts
    min 36 secs (0.01 hours)
    max 10 days
    """
    mean_hour = 0.2
    std_dev = 3
    d_hour = trunc_lognormvariate(mu=mean_hour, sigma=std_dev, min=0.01, max=240)
    d_sec = random.randrange(3600)

    return int((d_hour * 3600) + d_sec)


def trunc_lognormvariate(mu, sigma, min, max):
    val = max + 1

    while max < val or min > val:
        val = random.lognormvariate(mu=math.log(mu), sigma=math.log(sigma))

    return val


def parse_response(raw_text, thread_id):
    def split_lines(_str):
        result = []

        # for line in _str.split("\n")[1:]:
        for line in _str.splitlines():
            line = line.expandtabs().strip()
            if re.search(r"(\s\s+)", line):
                result.extend(split_lines(re.sub(r"(\s\s+)", r"\n", line)))
            else:
                result.append(line.strip())

        return result

    the_text = "\n".join(split_lines(raw_text))
    # print(the_text)

    str_io = StringIO(the_text)
    # try:
    # df = pd.read_csv(str_io, engine="python")
    # df = pd.read_csv(str_io)
    msg_ids = []
    usernames = []
    texts = []
    reader = csv.reader(str_io)
    for row in reader:
        # print(row)
        try:
            if len(row) > 0:
                if row[0] != "msg_id":
                    # msg_id, username, text = row
                    msg_ids.append(row[0])
                    usernames.append(row[1])
                    combined = ",".join(row[2:])
                    texts.append(combined)
        except:
            print("--------")
            print(row)
            print("--------")
            print(the_text)
            print("--------")

    df = pd.DataFrame(
        {
            "thread_id": thread_id,
            "msg_id": msg_ids,
            "username": usernames,
            "text": texts,
        }
    )

    return df


def create_normalised_thread_pool(in_file):
    in_df = pd.read_json(in_file)

    result_df = pd.DataFrame()

    for idx, row in in_df.iterrows():
        ic(idx)
        thread_id, number_of_msg, number_of_users, raw_text = row
        ic(thread_id, number_of_msg, number_of_users)
        df = parse_response(raw_text, thread_id)
        ic(len(df))
        result_df = pd.concat([result_df, df], ignore_index=True)
        # raise ValueError()

    result_df.to_json("normalised_thread_pool.json")
    print(result_df.head(50))


class AllUserPool:
    def __init__(self, max_num_users: int) -> None:
        self.max_num_users = max_num_users

    def get_user_selection(self, num_users):
        """returns a randomly selected group of `num_users` from the total pool of users"""
        user_ids = random.sample(range(self.max_num_users), k=num_users)
        return [f"gptchat_user_{id}" for id in user_ids]


def resample(total_samples, num_unique_users):
    """
    total_sample => The number of threads that in the resampled data
    num_unique_users => The number of unique users that will exist in the resampled data. Values smaller then the number of messages in a thread may cause ValueError to be raised.
    """
    # Load
    # generate_chat_text_dir = (
    #     Path(__file__).parent / ".." / ".." / ".." / "generate_chat_text"
    # )
    # generate_chat_text_dir = generate_chat_text_dir.resolve()

    thread_pool = pd.read_json(generate_chat_text_dir / "normalised_thread_pool.json")

    num_pool_threads = thread_pool["thread_id"].unique()
    username_pool = thread_pool["username"].unique()

    def clean_username(old):
        _s = old.lower()
        _s = re.sub("\W", "", _s, flags=re.ASCII)
        return _s.replace("_", "")

    username_striped = [clean_username(u) for u in username_pool]
    username_set = set(username_striped)
    # ic(username_striped)
    # ic(len(username_pool))
    # ic(len(username_set))

    all_user_pool = AllUserPool(num_unique_users)

    main_collection = pd.DataFrame()

    for sample_no in range(total_samples):
        # Pick thread
        # ic(sample_no)
        source_thread_id = random.choice(num_pool_threads)
        # ic(source_thread_id)
        source_thread = thread_pool[thread_pool["thread_id"] == source_thread_id].copy()

        # Apply dates
        new_timestamps = create_timestamps(len(source_thread))
        source_thread["timestamp"] = new_timestamps

        # Apply users
        users_from_thread = source_thread["username"].unique()
        demo_users = all_user_pool.get_user_selection(len(users_from_thread))
        user_name_map = {}

        for new_uname, old_uname in zip(demo_users, users_from_thread):
            user_name_map[old_uname] = new_uname

        source_thread["username"] = source_thread["username"].map(user_name_map)

        # Add to main
        if len(main_collection) > 0:
            main_collection = pd.concat(
                [main_collection, source_thread], ignore_index=True
            )
        else:
            main_collection = source_thread

    return main_collection


if __name__ == "__main__":
    # create_normalised_thread_pool("openai_thread_pool.json")
    df = resample(total_samples=1000, num_unique_users=75)
    df.to_json(generate_chat_text_dir / "main_collection.json")
