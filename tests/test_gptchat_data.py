import pytest
from icecream import ic
import pandas as pd

from long.data.gptchat_data import prep_gptchat_by_user_source


def test_prep_gptchat_by_user_source():
    source = prep_gptchat_by_user_source()
    assert source.name == "gptchat_by_user"
    ic(len(source.data))
    assert source.data is not None
    assert len(source.data) == 12911

    day_grouper = pd.Grouper(key=source.time_column, freq="1D")

    # by_user_all = source.get_aggregation(
    #     entity_group_by="username",
    #     time_grouper=day_grouper
    # )

    # assert len(by_user_all) == 8983
    # ic(by_user_all.head(20))

    # by_user_all = source.get_aggregation(
    #     entity_group_by="username",
    #     time_grouper=day_grouper,
    #     entity_permitted_values=["gptchat_user_0"]
    # )

    # by_user_all.index = by_user_all.index.droplevel("username")
    # # assert len(by_user_all) == 8983
    # ic(len(by_user_all))
    # ic(by_user_all.head(20))

    assert len(source.data) == 12911

    by_thread_all = source.get_aggregation(
        entity_group_by="thread_id",
        time_grouper=day_grouper,
        entity_permitted_values=[1],
    )

    # by_thread_all.index = by_user_all.index.droplevel("username")
    # assert len(by_user_all) == 8983
    ic(len(by_thread_all))
    ic(by_thread_all.head(20))

    pytest.fail("not complete")
