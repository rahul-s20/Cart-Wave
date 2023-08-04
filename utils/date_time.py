from datetime import datetime


def current_date() -> str:
    dt = datetime.now().strftime('%m%d%Y')
    return dt
