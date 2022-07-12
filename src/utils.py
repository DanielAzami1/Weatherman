from datetime import date, datetime


def get_current_time(pretty=True) -> str:
    in_time = datetime.now()
    converter = "%I:%M %p"
    out_time = in_time.time().strftime(converter)
    return out_time


def get_current_date() -> str:
    return str(date.today())

