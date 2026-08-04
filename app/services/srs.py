"""SM-2 spaced repetition helpers."""

from dataclasses import dataclass


@dataclass
class SRSState:
    interval: int = 1
    repetitions: int = 0
    ease_factor: float = 2.5


def update_sm2(state: SRSState, quality: int) -> SRSState:
    """Update a card state using a compact SM-2 style rule set."""

    quality = max(0, min(5, quality))
    if quality < 3:
        return SRSState(interval=1, repetitions=0, ease_factor=max(1.3, state.ease_factor - 0.2))

    repetitions = state.repetitions + 1
    if repetitions == 1:
        interval = 1
    elif repetitions == 2:
        interval = 6
    else:
        interval = round(state.interval * state.ease_factor)

    ease_factor = state.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    return SRSState(interval=interval, repetitions=repetitions, ease_factor=max(1.3, ease_factor))
