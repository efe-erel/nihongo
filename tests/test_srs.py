
from app.services.srs import calculate_next_review

def test_first_correct_review():
    """First review, quality 4 (correct) -> interval should be 1, repetitions 1."""
    repetitions, interval, ease_factor = calculate_next_review(
        quality=4, repetitions=0, interval=0, ease_factor=2.5
    )
    assert repetitions == 1
    assert interval == 1

def test_second_correct_review():
    """Second consecutive correct review -> interval should be 6."""
    repetitions, interval, ease_factor = calculate_next_review(
        quality=5, repetitions=1, interval=1, ease_factor=2.5
    )
    assert repetitions == 2
    assert interval == 6

def test_third_correct_review_uses_ease_factor():
    """Third+ correct review -> interval = previous_interval * ease_factor."""
    repetitions, interval, ease_factor = calculate_next_review(
        quality=4, repetitions=2, interval=6, ease_factor=2.6
    )
    assert repetitions == 3
    assert interval == round(6 * 2.6)  # 16

def test_forgotten_word_resets_repetitions():
    """Quality < 3 -> repetitions resets to 0, interval resets to 1."""
    repetitions, interval, ease_factor = calculate_next_review(
        quality=2, repetitions=3, interval=16, ease_factor=2.6
    )
    assert repetitions == 0
    assert interval == 1

def test_ease_factor_never_below_minimum():
    """Ease factor should never drop below 1.3."""
    repetitions, interval, ease_factor = calculate_next_review(
        quality=3, repetitions=5, interval=10, ease_factor=1.3
    )
    assert ease_factor >= 1.3

def test_invalid_quality_raises_error():
    """Quality outside 0-5 range should raise ValueError."""
    import pytest
    with pytest.raises(ValueError):
        calculate_next_review(quality=10, repetitions=0, interval=0, ease_factor=2.5)