from __future__ import annotations

from typing import List, Tuple

# TODO this could just be a list and not a bool, as empty lists are falsy
validator_result_type = Tuple[bool, List[str]]
