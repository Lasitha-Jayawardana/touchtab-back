def split_full_name(full_name):
    # Split the full name into a list of words
    name_list = full_name.split()

    # Extract the first name (index 0) and last name (index -1 if exists, otherwise None)
    first_name = name_list[0]
    last_name = name_list[-1] if len(name_list) > 1 else None

    return (first_name, last_name)
