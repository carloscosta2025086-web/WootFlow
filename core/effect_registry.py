"""Central effect registry for runtime usage."""

from core.effects_engine import EFFECTS as _EFFECTS
from core.effects_engine import EFFECT_NAMES as _EFFECT_NAMES

EFFECT_REGISTRY = dict(_EFFECTS)
EFFECT_LABELS = dict(_EFFECT_NAMES)


def get_effect_class(name: str):
    return EFFECT_REGISTRY.get(name)


def list_effect_items():
    return sorted(EFFECT_LABELS.items(), key=lambda pair: pair[1].lower())
