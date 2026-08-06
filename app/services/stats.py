
from datetime import date, timedelta

def calculate_streak(review_dates: list[date]) -> int:

    if not review_dates:
        return 0

    dates_set = set(review_dates)
    today = date.today()

    if today in dates_set:
        streak = 1
        check_date = today - timedelta(days=1)

    elif (today - timedelta(days=1)) in dates_set:
        streak = 1
        check_date = today - timedelta(days=1)

    else:
        return 0

    while check_date in dates_set:
        streak += 1
        check_date -= timedelta(days=1)

    return streak