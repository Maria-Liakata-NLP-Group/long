

class Source():
    # self.name = ""
    # self.user_ids = []
    # self.cmoc_methods = [] # List[str] of method_ids

    def __init__(self, name, data_daily_interactions, all_cmocs):
        self.name = name
        self.data_daily_interactions = data_daily_interactions
        self.all_cmocs = all_cmocs

        self.user_ids = list(data_daily_interactions.keys())
        self.cmoc_methods = list(all_cmocs.keys())

    def get_user_df(self, user_id: str):
        cmocs_as_df = self.data_daily_interactions[user_id].copy()
    
        for method_name in self.cmoc_methods:
            cmocs_as_df = self._add_cmoc_cols(cmocs_as_df, method_name, user_id)

        return cmocs_as_df

    def cmoc_method_friendly_names(self, method_id: str) -> str:
        return method_id.replace("_", " ").title()


    def _add_cmoc_cols(self, user_df, method_name: str, user_id):
        user_df[method_name] = None

        sample_cmocs = self.all_cmocs[method_name]
        sample_tl_cmocs = sample_cmocs[user_id]

        user_df[method_name] = user_df.apply(
            lambda x: 1 if (x.name.date() in sample_tl_cmocs) else None,
            axis=1)

        return user_df