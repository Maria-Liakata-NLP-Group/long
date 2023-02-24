from .random_data import random_data
from .source import AggregateSource
import sys
from icecream import ic
from pathlib import Path
from .gptchat_data import gptchat_by_user_source, gptchat_by_thread_source

_available_sources = {}

try:
    TL_GENERATION_PATH = Path("../anthony/timeline_generation").absolute().resolve()

    ic(TL_GENERATION_PATH)
    sys.path.append(str(TL_GENERATION_PATH))

    from .tl_generation_wrapper import talk_life_aggregate

    _available_sources[talk_life_aggregate.name] = talk_life_aggregate
except ImportError as ie:
    print("!!!!!!!!!!!")
    print("Unable to load Talklife data")
    print(sys.path)
    print(ie)
    print("!!!!!!!!!!!")


# Ensure that there is at least one data source
_available_sources[gptchat_by_user_source.name] = gptchat_by_user_source
_available_sources[gptchat_by_thread_source.name] = gptchat_by_thread_source
_available_sources[random_data.name] = random_data


def list_source_names() -> AggregateSource:
    return _available_sources.keys()


def get_all_sources():
    return _available_sources.values()


def get_source(source_name: str) -> AggregateSource:
    return _available_sources[source_name]
