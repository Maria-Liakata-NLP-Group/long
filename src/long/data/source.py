from icecream import ic
import pandas as pd
from typing import List, Union, Optional


class Source:
    def __init__(
        self,
        name,
        data: pd.DataFrame,
        unique_id_column: str,
        parent_id_column: str,
        entity_columns: List[str],
        time_column: str = None,
        cmoc_columns: Optional[List[str]] = None,
    ):
        self.name = name
        self._df: pd.DataFrame
        if data is None:
            self._df = pd.DataFrame()
        else:
            self._df = data

        # self._verify_unique_id_column()
        if unique_id_column is not None:
            self._unique_id_column: str = unique_id_column

        self.entity_columns: List[str] = entity_columns

        if time_column is not None:
            self.time_column: str = time_column
        self._cmoc_columns: List[str] = []

    def _verify_unique_id_column(self, column_name: str):
        if self._unique_id_column is not None:

            if column_name not in self._df.columns:
                raise ValueError(
                    f"Column {column_name} not in dataframe columns {self._df.columns}"
                )

            if not self._df[column_name].is_unique:
                raise ValueError(f"Column {column_name} is not unique")

    @property
    def entity_columns(self) -> List[str]:
        return self._entity_columns

    @entity_columns.setter
    def entity_columns(self, value: Union[str, List[str]]):
        # Ensure value is a list
        if isinstance(value, str):
            value = [value]

        if any([val not in self._df.columns for val in value]):
            raise ValueError(
                f"One or more column in {value} are not in the dataframe columns {self._df.columns}"
            )

        self._entity_columns = value

    @property
    def time_column(self) -> str:
        return self._time_column

    @time_column.setter
    def time_column(self, value: str):
        if value not in self._df.columns:
            raise ValueError(f"Column {value} not in dataframe")

        ic(self._df[value].dtype)

        if self._df[value].dtype != "datetime64[ns]":
            raise ValueError(f"Column {value} is not of type datetime64[ns]")

        self._time_column = value

    @property
    def cmoc_columns(self):
        return self._cmoc_columns

    @cmoc_columns.setter
    def cmoc_columns(self, value):
        pass

    @property
    def data(self):
        """
        Allows raw access to the dataframe.
        This is unsafe, as it allows the user to modify the dataframe
        without going through the Source class.
        Use with caution.
        """
        return self._df

    def _apply_time_range(
        self, date_range: tuple[pd.Timestamp, pd.Timestamp | pd.Timedelta]
    ):
        arg1, arg2 = date_range
        if isinstance(arg2, pd.Timedelta):
            min_date = arg1
            max_date = arg1 + arg2

        else:
            min_date = min(arg1, arg2)
            max_date = max(arg1, arg2)

        return self._df[
            (self._df[self.time_column] >= min_date)
            & (self._df[self.time_column] <= max_date)
        ]

    def get_aggregation(
        self,
        entity_group_by: str,
        time_grouper: pd.Grouper,
        entity_permitted_values: Optional[str | List[str]] = None,
        date_range: Optional[
            tuple[pd.Timestamp, pd.Timestamp | pd.tseries.offsets.DateOffset]
        ] = None,
    ):
        """
        - [ ] whole timeline
          - [x] aggregation by thread
          - [x] aggregation by timestep (use pd.Grouper https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#grouping-with-a-grouper-specification)
          - [ ] (optional) filtered by threads started by that user (where parent_thread_id == root)
          - [x] (optional) filtered per timerange

        - [x] whole timeline
          - [x] aggregation by user
          - [x] aggregation by timestep
          - [x] filtered per thread
          - [x] (optional) filtered per timerange

        *
        # TODO: This currently returns a dataframe, which has been aggregated.
        However it would be more consistent to return an instance of an AgrregateSource object

        """
        # Check that the entity columns is
        if entity_group_by not in self._entity_columns:
            raise ValueError(f"{entity_group_by} not in {self._entity_columns}")

        if date_range is not None:
            # We need to look at how the date_range interacts with the time_grouper
            # Is there an offset that needs to be accommodated to ensure that the
            # aggregation is correct for the being and end of the date_range?
            # For now we'll just attempt to catch any non-standard time_grouper offsets
            # and raise an error.
            if time_grouper.offset is not None:
                raise ValueError(
                    "Unsupported pd.Grouper values. time_grouper.offset must be None"
                )

            if time_grouper.origin != "start_day":
                raise ValueError(
                    "Unsupported pd.Grouper values. time_grouper.origin must be 'start_day'"
                )

            _df = self._apply_time_range(date_range)
        else:
            _df = self._df

        _df = _df.copy()

        # ic(_df.columns)

        if entity_permitted_values is not None:
            # Ensure entity_permitted_values is a list
            if isinstance(entity_permitted_values, str):
                entity_permitted_values = [entity_permitted_values]

            _df = _df[_df[entity_group_by].isin(entity_permitted_values)]

        # _df = _df.sort_values(by=self.time_column, ascending=True)
        # ic(_df.columns)

        ic(entity_permitted_values)
        ic(len(_df))
        # ic(_df.head())
        # Now we can group by the entity and time
        # ic([entity_group_by, time_grouper])
        grouped = _df.groupby([entity_group_by, time_grouper])
        # ic(grouped.groups.keys())
        # ic(grouped.head())
        result = grouped.sum()

        return result


class AggregateSource:
    # self.name = ""
    # self.user_ids = []
    # self.cmoc_methods = [] # List[str] of method_ids

    def __init__(self, name, data_daily_interactions, all_cmocs):
        self.name = name
        self.full_timeline_df = None
        self.data_daily_interactions = data_daily_interactions
        self.all_cmocs = all_cmocs

        self.user_ids = list(data_daily_interactions.keys())

        self.cmoc_methods = list(all_cmocs.keys())

    def get_user_df(self, user_id: str):
        try:
            cmocs_as_df = self.data_daily_interactions[user_id].copy()

            for method_name in self.cmoc_methods:
                cmocs_as_df = self._add_cmoc_cols(cmocs_as_df, method_name, user_id)

            cmocs_as_df.sort_values(by="timestamp", inplace=True)
            return cmocs_as_df
        except KeyError:
            return pd.DataFrame()

    def get_full_user_timeline(self, user_id_dd):

        if self.full_timeline_df is None:
            ic()
            return None

        if isinstance(user_id_dd, str):
            user_id = ic(user_id_dd)
        else:
            user_id = ic(user_id_dd["props"]["value"])
        ic(self.full_timeline_df.head())
        full_user_tl = self.full_timeline_df[
            self.full_timeline_df["username"] == user_id
        ].copy()
        ic(len(full_user_tl))
        return full_user_tl

    def cmoc_method_friendly_names(self, method_id: str) -> str:
        """
        Maps the method_id (the internal identifier for the method) to a human readable name.

        params: method_id: either a single method_id str.

        returns: The method_id with "_" char replaced by spaces and the str switched to Title case.
        """
        return method_id.replace("_", " ").title()

    def _add_cmoc_cols(self, user_df, method_name: str, user_id):
        user_df[method_name] = None

        sample_cmocs = self.all_cmocs[method_name]
        sample_tl_cmocs = sample_cmocs[user_id]

        user_df[method_name] = user_df.apply(
            lambda x: 1 if (x.name.date() in sample_tl_cmocs) else None, axis=1
        )

        return user_df
