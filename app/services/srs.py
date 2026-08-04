
def calculate_next_review(quality: int, repetitions: int, interval: int, ease_factor: float) -> tuple[int, int, float]:

    """
    Calculates the next review parameters based on the SuperMemo 2 algorithm.

    Args:
        quality: User's recall quality, 0-5 (0 = complete blackout, 5 = perfect recall)
        repetitions: Number of consecutive correct answers so far
        interval: Current interval in days
        ease_factor: Current ease factor (starts at 2.5)

    Returns:
        A tuple of (new_repetitions, new_interval, new_ease_factor)
    """
    
    if not 0 <= quality <= 5:
        raise ValueError("quality must be between 0 and 5")
    
    if quality < 3:
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = round(interval * ease_factor)


        repetitions += 1
        ease_factor += (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        if ease_factor < 1.3:
            ease_factor = 1.3

    return repetitions, interval, ease_factor