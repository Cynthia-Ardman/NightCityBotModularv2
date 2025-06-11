from typing import Dict

ROLE_COSTS_BUSINESS: Dict[str, int] = {
    "Business Tier 0": 0,
    "Business Tier 1": 2000,
    "Business Tier 2": 3000,
    "Business Tier 3": 5000
}

ROLE_COSTS_HOUSING: Dict[str, int] = {
    "Housing Tier 1": 1000,
    "Housing Tier 2": 2000,
    "Housing Tier 3": 3000
}

TRAUMA_ROLE_COSTS: Dict[str, int] = {
    "Trauma Team Silver": 1000,
    "Trauma Team Gold": 2000,
    "Trauma Team Plat": 4000,
    "Trauma Team Diamond": 10000
}

BASELINE_LIVING_COST: int = 500