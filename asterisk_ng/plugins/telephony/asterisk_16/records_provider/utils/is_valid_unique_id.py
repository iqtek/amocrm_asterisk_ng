__all__ = [
    "is_valid_unique_id",
]


def is_valid_unique_id(unique_id: str) -> bool:
    separator_index = unique_id.find('.')

    if separator_index == -1:
        return False

    unix_time_str = unique_id[0: separator_index]
    call_number = unique_id[separator_index + 1:]
    return unix_time_str.isdigit() and call_number.isdigit()
