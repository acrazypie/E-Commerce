import re

FORBIDDEN_WORDS = {"admin", "root", "test", "cheesecake"}


def is_valid_username(username: str) -> bool:
    return re.fullmatch(r"[A-Za-z]{3,}$", username) is not None


def is_clean_username(username: str) -> bool:
    return username.lower() not in FORBIDDEN_WORDS


def validate_username(username: str) -> bool:
    return is_valid_username(username) and is_clean_username(username)
