"""Quest model helpers for capability-gated tooling."""

QUEST3_MODEL = "Quest 3"
QUEST3S_MODEL = "Quest 3S"
QUEST3_FAMILY_MODELS = {QUEST3_MODEL, QUEST3S_MODEL}


def is_quest3_family(model):
    return model in QUEST3_FAMILY_MODELS


def require_quest3_family(model, feature):
    if not is_quest3_family(model):
        raise RuntimeError(f"{feature} requires a Quest 3/3S headset, found {model or 'unknown'}")


def require_quest3_only(model, feature):
    if model != QUEST3_MODEL:
        raise RuntimeError(f"{feature} is Quest 3-only, found {model or 'unknown'}")
