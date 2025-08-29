def validate_fullname(fullname):
    fullname = fullname.strip()

    if not fullname.replace(" ", "").isalpha():
        return None
    
    fullname_parts = fullname.split()

    if not 0 < len(fullname_parts) < 3:
        return None

    return fullname_parts


def mask_fullname(fullname):
    parts = validate_fullname(fullname)
    
    if not parts:
        return "Invalid name"
    
    if len(parts) == 1:
        first_name = parts[0]
        if len(first_name) < 2:
            return "Invalid name"
        return first_name[0].upper() + "***"
    
    first_name, last_name = parts

    if len(first_name) < 2 or len(last_name) < 2:
        return "Invalid name"

    first_name = first_name[0].upper() + "***"
    last_name = last_name[0].upper() + "***"

    return f"{first_name} {last_name}"
