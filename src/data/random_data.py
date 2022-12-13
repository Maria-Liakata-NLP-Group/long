import random
from itertools import accumulate
from typing import Dict, List

import pandas as pd
from icecream import ic

from .source import Source

data_daily_interactions = {}
date_range = pd.date_range(start="2017-01-01", end="2021-01-01")
# ic(len(date_range))

all_cmocs: Dict[str, Dict[str, List[pd.Timestamp]]] = {}

cmoc_random_values = [3, 30, 100]

for num_cmoc in cmoc_random_values:
    all_cmocs[f"random_{num_cmoc}"] = {}

for user_num in range(12):
    user_id = f"random_user_{user_num}"

    # np.random.seed(user_num)
    random.seed(user_num)
    day_delta = [random.normalvariate(-1, 4) for _ in range(len(date_range))]

    # paretovariate
    def sum_if_pos(x, y):
        return int(max(0, x + y))

    posts = list(accumulate(day_delta, func=sum_if_pos))
    # posts = list(accumulate(day_delta))
    # posts = day_delta
    data_daily_interactions[user_id] = pd.DataFrame(
        {"posts": posts},
        index=date_range,
    )

    for num_cmoc in cmoc_random_values:
        gen_cmocs = random.choices(date_range, weights=posts, k=num_cmoc)

        cmoc_lst = [_date for _date in gen_cmocs]
        # ic(user_id)
        # ic(cmoc_lst)

        # user_cmocs = {}
        # user_cmocs[user_id] = gen_cmocs

        all_cmocs[f"random_{num_cmoc}"][user_id] = gen_cmocs

    # all_cmocs = {}

random_data = Source("random_data", data_daily_interactions, all_cmocs)
