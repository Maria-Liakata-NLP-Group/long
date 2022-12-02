from .source import Source
import pandas as pd
import random
from icecream import ic
from itertools import accumulate

data_daily_interactions = {}
date_range = pd.date_range(start="2019-01-01",end="2021-12-31")
ic(len(date_range))

all_cmocs = {}
all_cmocs["random_3"] = {}

for user_num in range(12):
    user_id = f"random_user_{user_num}"

    # np.random.seed(user_num)
    random.seed(user_num)
    day_delta = [random.normalvariate(-1, 4) for _ in range(len(date_range))]

    # paretovariate
    sum_if_pos = lambda x,y: int(max(0, x+y))
        
    posts = list(accumulate(day_delta, func=sum_if_pos))
    # posts = list(accumulate(day_delta))
    # posts = day_delta
    data_daily_interactions[user_id] = pd.DataFrame({"posts": posts}, index=date_range,)


    gen_cmocs = random.choices(date_range, weights=posts, k=3)
  
    cmoc_lst = [_date for _date in gen_cmocs]
    ic(user_id)
    ic(cmoc_lst)

    # user_cmocs = {}
    # user_cmocs[user_id] = gen_cmocs

    all_cmocs["random_3"][user_id] = gen_cmocs

    # all_cmocs = {}

random_data = Source("random_data", data_daily_interactions, all_cmocs)