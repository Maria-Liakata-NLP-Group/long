import pytest
from icecream import ic
import pandas as pd

from long.data.gptchat_data import prep_gptchat_by_user_source


@pytest.mark.xfail(
    reason=(
        "Unknown reason for failure. Each call to `source.get_aggregation` _*should*_ "
        "return a new independent dataframe. The order of the tests should _*not*_ "
        "matter."
        "However multiple calls do results in intermittent failures."
        " `ValueError: all keys need to be the same shape` is raised by the underlying `grouped.count()` method."
        ""
        "As a minimal example, this example passes:"
        " `for thread_id in [211, 97, 41]`"
        ""
        "However, by simply reordering the list, the example fails:"
        " `for thread_id in [97, 41, 211]`"
        ""
        "See https://github.com/Maria-Liakata-NLP-Group/long/issues/64"
    )
)
def test_prep_gptchat_by_user_source():
    source = prep_gptchat_by_user_source()
    assert source.name == "gptchat_by_user"
    # ic(len(source.data))
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
    # ic(source.data[["thread_id"]].describe())

    error_count = 0

    # for thread_id in source.data["thread_id"].unique():
    # for thread_id in [97, 41, 211]:
    for thread_id in [211, 97, 41]:

        # ic(thread_id)
        # ic(type(thread_id))

        # temp = source.data[source.data["thread_id"]==thread_id]

        # assert len(temp) > 0
        # ic(temp.head(1))

        try:
            by_thread_all = source.get_aggregation(
                entity_group_by="thread_id",
                time_grouper=day_grouper,
                entity_permitted_values=[thread_id],
            )
        except ValueError as e:
            ic(e)
            ic(thread_id)
            # ic(type(thread_id))
            # ic(len(temp))
            # ic(temp.head())
            error_count += 1
            raise e

        # if len(by_thread_all) == 2:
        #     ic(thread_id)
        #     assert False

    # Example thread_id's
    # 1 => only one message
    # 211 => 4 msg

    # by_thread_all.index = by_user_all.index.droplevel("username")
    # assert len(by_user_all) == 8983
    # ic(len(by_thread_all))
    # ic(by_thread_all.head(20))
    ic(error_count)

    pytest.fail("not complete")
