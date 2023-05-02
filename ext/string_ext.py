import datetime


def format_string_to_date_sqlite(date_string: str) -> str:
    d = datetime.datetime.strptime(date_string, '%d-%m-%Y')
    return datetime.date.strftime(d, "%Y-%m-%d")
