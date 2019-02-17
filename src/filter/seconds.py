import numpy as np
from typing import List, Dict, Any, Optional, Tuple


def get_fixed_tempo_estimate(tempomap: List[Dict[float, Any]]):
    return np.median(tempomap)
