from core.effect_registry import EFFECT_LABELS, EFFECT_REGISTRY, get_effect_class


def test_registry_has_core_effects():
    assert "breathing" in EFFECT_REGISTRY
    assert "breathing" in EFFECT_LABELS


def test_registry_returns_effect_class():
    cls = get_effect_class("breathing")
    assert cls is not None
    instance = cls()
    assert hasattr(instance, "update")
