import asyncio


def notify(hours: str, minutes: str, seconds: str) -> str:

    """Notifies the user they will be reminded after their
    inputted amount of time has passed. This should only be
    called after the input is validated."""

    h = f'{int(hours)} hours, ' if hours != "1" else f'{int(hours)} hour, '
    m = f'{int(minutes)} minutes, and ' if minutes != "1" else f'{int(minutes)} minute, and '
    s = f'{int(seconds)} seconds.' if seconds != "1" else f'{int(seconds)} second.'

    # setup embed to confirm with user
    return "I will remind you in: " + h + m + s


async def remind(hours: str, minutes: str, seconds: str, mention: str) -> str:

    """ this reminds the user about their pick after X amount of time."""

    waiting_time = 3600 * int(hours) + 60 * int(minutes) + int(seconds)
    await asyncio.sleep(waiting_time)
    return mention


def valid_time_input(hours: str, minutes: str, seconds: str) -> bool:

    """Ensures the time entered is valid."""

    # valid time constants
    SECOND_COUNT_FLOOR = 0
    SECOND_COUNT_CEILING = 59
    MINUTE_COUNT_FLOOR = 0
    MINUTE_COUNT_CEILING = 59
    HOUR_COUNT_FLOOR = 0
    HOUR_COUNT_CEILING = 48

    return (hours.isdigit() and minutes.isdigit() and seconds.isdigit()
            and HOUR_COUNT_FLOOR <= int(hours) <= HOUR_COUNT_CEILING
            and MINUTE_COUNT_FLOOR <= int(minutes) <= MINUTE_COUNT_CEILING
            and SECOND_COUNT_FLOOR <= int(seconds) <= SECOND_COUNT_CEILING)
