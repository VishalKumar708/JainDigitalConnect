import re


def is_valid_blood_group(value):
    # Define a regular expression pattern for a blood group
    blood_group_pattern = r'^\s*(A|B|AB|O)\s*[+-]?\s*$'

    return bool(re.match(blood_group_pattern, value, re.IGNORECASE))
