import pytest
from long.data import source
import pandas as pd
from icecream import ic


@pytest.fixture
def example_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "user_id": ["a", "a", "b", "b", "b", "b"],
            "date": [
                pd.Timestamp("2020-01-01T01:23"),
                pd.Timestamp("2020-01-02T04:56"),
                pd.Timestamp("2020-01-01T09:12"),
                pd.Timestamp("2020-01-02T03:45"),
                pd.Timestamp("2020-01-02T06:21"),
                pd.Timestamp("2020-02-03T08:32"),
            ],
            "thread_id": ["1", "1", "2", "2", "2", "2"],
            "posts": [1, 2, 3, 4, 5, 6],
        }
    )


@pytest.fixture
def example_source(example_df) -> source.Source:
    return source.Source(
        name="test_source",
        data=example_df,
        unique_id_column=None,
        parent_id_column=None,
        entity_columns=["user_id", "thread_id"],
        time_column="date",
    )


def test_source_constructor(example_df):
    actual_source = source.Source(
        name="test_source",
        data=example_df,
        unique_id_column=None,
        parent_id_column=None,
        entity_columns=["user_id", "thread_id"],
        time_column="date",
    )
    assert actual_source.name == "test_source"
    assert example_df.compare(actual_source.data).empty
    assert actual_source.cmoc_columns == []

    # _source = source.Source("test_source2", None)
    # assert _source.name == "test_source2"
    # assert isinstance(_source.data, pd.DataFrame)


@pytest.mark.skip("not implemented")
def test_source_time_aggregation():
    pass


def test_source_entity_columns(example_source):
    failing_wrong_type_columns = ["user_id", "date"]
    failing_non_existant_columns = ["user_id", "non_existant_column"]
    passing_entity_columns = ["user_id", "thread_id"]

    with pytest.raises(ValueError, match="not in the dataframe columns"):
        example_source.entity_columns = failing_non_existant_columns

    example_source.entity_columns = passing_entity_columns
    assert example_source.entity_columns == passing_entity_columns


@pytest.mark.parametrize(
    "entity_group_by,freq,entity_filter,date_range,expected_result",
    [
        ("user_id", "D", None, None, {"thread_id": [1, 1, 1, 2, 1]}),
        ("thread_id", "2D", None, None, {"user_id": [2, 3, 1]}),
        (
            "user_id",
            "2D",
            ["a"],
            (pd.Timestamp("2020-01-01"), pd.Timestamp("2020-01-03")),
            {"thread_id": [2]},
        ),
        (
            "user_id",
            "2D",
            "a",
            (pd.Timestamp("2020-01-01"), pd.Timestamp("2020-01-02")),
            {"thread_id": [1]},
        ),
    ],
    ids=[1, 2, 3, 4],
)
def test_get_aggregation(
    example_source, entity_group_by, freq, entity_filter, date_range, expected_result
):

    ic(example_source.entity_columns)

    actual = example_source.get_aggregation(
        entity_group_by=entity_group_by,
        time_grouper=pd.Grouper(key=example_source.time_column, freq=freq),
        entity_permitted_values=entity_filter,
        date_range=date_range,
    )
    ic(actual)

    for key, expected_value in expected_result.items():
        assert actual[key].tolist() == expected_value


@pytest.mark.xfail(reason="time grouper offset not implemented yet")
@pytest.mark.parametrize(
    "grouper_args,expected_result",
    [
        ({"offset": "8H"}, None),
        ({"origin": "start"}, None),
    ],
)
def test_get_aggregation_with_offset(example_source, grouper_args, expected_result):

    actual = example_source.get_aggregation(
        entity_group_by="user_id",
        time_grouper=pd.Grouper(
            key=example_source.time_column, freq="2D", *grouper_args
        ),
        entity_permitted_values=None,
        date_range=None,
    )


def test_apply_time_range(example_source):
    date1 = pd.Timestamp("2020-01-01")
    date2 = pd.Timestamp("2020-01-02")
    offset1 = pd.Timedelta("1D")
    offset2 = pd.Timedelta("40D")

    range_1 = (date1, date2)
    range_2 = (date2, date1)
    range_3 = (date2, offset1)
    range_4 = (date1, offset2)

    # Each tuple is the range and the expected number of rows
    test_cases = [
        (range_1, 2),
        (range_2, 2),
        (range_3, 3),
        (range_4, 6),
    ]

    for range_, expected in test_cases:
        actual_df = example_source._apply_time_range(range_)
        ic(actual_df)
        assert actual_df.shape[0] == expected


@pytest.mark.skip("not implemented")
def test_source_add_cmoc_cols():
    pass


@pytest.mark.skip("not implemented")
def test_source_get_cmoc_method_friendly_names():
    pass
