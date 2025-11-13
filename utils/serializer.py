from datetime import datetime, date
import numpy as np
import math

def fix_types(obj):
    """Convert non-JSON-safe types to JSON friendly values."""
    if isinstance(obj, list):
        return [fix_types(x) for x in obj]
    if isinstance(obj, dict):
        return {k: fix_types(v) for k, v in obj.items()}
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return datetime(obj.year, obj.month, obj.day).isoformat()
    if isinstance(obj, float):
        return None if math.isnan(obj) or math.isinf(obj) else obj
    if isinstance(obj, np.generic):
        return obj.item()
    return obj
