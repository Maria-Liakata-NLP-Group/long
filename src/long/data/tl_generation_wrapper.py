import sys
from pathlib import Path

from icecream import ic

from .source import AggregateSource

TL_GENERATION_PATH = Path("../anthony/timeline_generation").absolute().resolve()

ic(TL_GENERATION_PATH)
sys.path.append(str(TL_GENERATION_PATH))

try:
    from utils.io.my_pickler import my_pickler
    from utils.visualize.plot_results import method_name_mapper

    data_daily_interactions = my_pickler(
        "i", "observed_data_daily_interactions", folder="datasets"
    )

    all_cmocs = my_pickler("i", "candidate_moments_of_change", folder="datasets")

    _source = AggregateSource("talklife-aggregated", data_daily_interactions, all_cmocs)
    # _source.cmoc_method_friendly_names = lambda n:

    def method_name_wrapper(method_id: str) -> str:
        try:
            return method_name_mapper([method_id])[method_id]
        except KeyError:
            return method_id.replace("_", " ").title()

    ic(_source.cmoc_methods)

    _source.cmoc_method_friendly_names = method_name_wrapper
    talk_life_aggregate = _source

except Exception as ex:
    print(ex)
