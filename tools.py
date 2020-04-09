import json


def build_tables(json_filename, fields):
    """
    Build tables from a text file, sorting each entry into categories based on fields.

    The text file contains the entries from a dice roll table in the following format:
    [number] [entry for field 1] [entry for field 2] [entry for field 3] etc.
    Example:
    42 Globe History Gyrating I- -kang
    """
    # Each field will get its own blank table. This variable is a dict of dicts.
    tables = {table_name: {} for table_name in fields}

    # Strip the JSON extension from the filename and add a TXT extension.
    # We do this so that build_tables can be called with the same filename used for
    # load_tables.
    text_filename = json_filename[:-5]
    text_filename += ".txt"

    try:
        with open(text_filename, "r") as file:
            for line in file:
                cleaned_line = line.strip()
                # Split the set of entries by field.
                entry = cleaned_line.split(" ")
                # Get the number for this set of entries.
                number = int(entry[0])

                # Match each entry to its corresponding field.
                for table, item in zip(tables.values(), entry[1:]):
                    table[number] = item
    except FileNotFoundError:
        raise FileNotFoundError(
            "Couldn't find a text file named {} with table data!".format(text_filename)
        )

    save_tables(tables, json_filename)


def save_tables(tables, filename):
    """
    Save tables to the specified JSON file.
    """
    json_tables = {label.value: inner_table for label, inner_table in tables.items()}

    with open(filename, "w") as file:
        json.dump(json_tables, file)


def load_tables(filename, fields):
    """
    Load tables from a JSON file, adjusting their keys to be integers.
    """
    try:
        with open(filename, "r") as file:
            json_tables = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("No JSON file named {}!".format(filename))

    # Loading JSON will always give us string keys, and we need integers.
    labeled = {fields(int(num)): table for num, table in json_tables.items()}
    # Since each key references a value that is itself a table, we need to correct
    # the inner table keys to be integers as well.
    for key, inner_table in labeled.items():
        labeled[key] = {int(k): v for k, v in inner_table.items()}

    return labeled


def build_item_tables(json_filename, fields):
    """
    Build item tables from a text file.

    The text file contains entries from a dice roll table in the following format:
    [number or number range] [item type]
    Example:
    42-46 Hammer
    """
    # TODO If number range, top_end - bottom_end + 1 will be weight of that entry.
    # If not number range, weight is 1.
    raise NotImplementedError(
        "Haven't figured out how to do this yet. Need to set format of text file(s)"
    )

    # # Each field will get its own blank table. This variable is a dict of dicts.
    # tables = {table_name: {} for table_name in fields}

    # # Strip the JSON extension from the filename and add a TXT extension.
    # # We do this so that build_item_tables can be called with the same filename used for
    # # load_tables.
    # text_filename = json_filename[:-5]
    # text_filename += ".txt"

    # try:
    #     with open(text_filename, "r") as file:
    #         for line in file:
    #             cleaned_line = line.strip()
    #             # Split the entry from the number for the entry.
    #             entry = cleaned_line.split(" ")
    #             # Get the number or number range for this entry.
    #             number_range = get_number_range(entry[0])

    #             # Match each entry to its corresponding field.
    #             for table, item in zip(tables.values(), entry[1:]):
    #                 table[number] = item

    # except FileNotFoundError:
    #     raise FileNotFoundError(
    #         "Couldn't find a text file named {} with table data!".format(text_filename)
    #     )

    # save_tables(tables, json_filename)


def get_number_range(number_string):
    """
    Returns integers representing the endpoints of the range indicated in number_string.
    If number_string is a single number, these endpoints will be 1 apart.
    The high endpoint is not inclusive for compatibility with Python's range() function.
    If the range is 76-100, low = 76 and high = 101. If the range is 41, low = 41 and
    high = 42.
    """
    if number_string.contains("-"):
        number_range = number_string.split("-")
        low = int(number_range[0])
        high = int(number_range[1]) + 1
    else:
        low = int(number_string)
        high = low + 1

    return (low, high)
