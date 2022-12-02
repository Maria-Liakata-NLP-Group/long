from pathlib import Path
import sys
from icecream import ic
from .source import Source

TL_GENERATION_PATH = Path("../anthony/timeline_generation").absolute().resolve()
ic(TL_GENERATION_PATH)
sys.path.append(str(TL_GENERATION_PATH))

from utils.io.my_pickler import my_pickler

data_daily_interactions = my_pickler(
    "i", "observed_data_daily_interactions", folder="datasets"
)

all_cmocs = my_pickler(
    "i", "candidate_moments_of_change", folder="datasets"
)

talk_life_aggregate = Source("talklife-aggregated", data_daily_interactions, all_cmocs)
