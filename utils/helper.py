import bcrypt
from datetime import datetime


def hashing(content: str):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes(content, 'utf-8'), salt)
    return hashed.decode("utf-8")


def check_hash(content: str, hashed_content: str) -> bool:
    return bcrypt.checkpw(bytes(content, 'utf-8'), bytes(hashed_content, 'utf-8'))


def filter_objects(obj, fields: set):
    if all(name in obj for name in fields):
        return obj
    else:
        raise ValueError("Keys are not matching")


def current_date() -> str:
    dt = datetime.now().strftime('%m%d%Y')
    return dt


def current_date_time() -> str:
    dt = datetime.now().strftime('%m%d%Y_%H%M%S')
    return dt
