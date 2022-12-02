
from .source import Source
from .random_data import random_data 


_available_sources = {}

try:
    import tl_generation_wrapper as tl
    _available_sources[tl.talk_life_aggregate.name] = tl.talk_life_aggregate
except ImportError:
    pass

# Ensure that there is at least one data source
_available_sources[random_data.name] = random_data

def list_source_names() -> Source:
    return _available_sources.keys()

def get_all_sources():
    return _available_sources.values()

def get_source(source_name: str) -> Source:
    return _available_sources[source_name]
