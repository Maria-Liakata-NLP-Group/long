from icecream import ic
import pandas as pd


class Source:
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
