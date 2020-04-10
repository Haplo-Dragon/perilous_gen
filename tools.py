import json
import tables


def build_tables(json_filename, fields):
    """
    Build tables from a text file, sorting each entry into categories based on fields.

    The text file contains the entries from a dice roll table in the following format:
    [number] [entry for field 1] [entry for field 2] [entry for field 3] etc.
    Example:
    42 Globe History Gyrating I- -kang
    """
    # Each field will get its own blank table. This variable maps enum members to
    # Table objects.
    enum_tables = {table_name: tables.Table() for table_name in fields}

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
                # Get the weight for this set of entries.
                # For ranges, weight = top - bottom + 1. For single numbers, weight = 1.
                weight = number_to_weight(entry[0])

                # Match each entry to its corresponding field.
                for table, item in zip(enum_tables.values(), entry[1:]):
                    table.entries.append(item)
                    table.weights.append(weight)

    except FileNotFoundError:
        raise FileNotFoundError(
            "Couldn't find a text file named {} with table data!".format(text_filename)
        )

    save_tables(enum_tables, json_filename)


def save_tables(enum_tables, filename):
    """
    Save tables to the specified JSON file.
    """
    # Since enum members can't be JSONified, we'll use their numerical values as keys.
    json_tables = {}
    for label, inner_table in enum_tables.items():
        json_tables[label.value] = {
            'entries': inner_table.entries,
            'weights': inner_table.weights}

    with open(filename, "w") as file:
        json.dump(json_tables, file)


def load_tables(filename, fields):
    """
    Load tables from a JSON file, adjusting their keys to be enum members and their
    values to be Table objects.
    """
    try:
        with open(filename, "r") as file:
            json_tables = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("No JSON file named {}!".format(filename))

    # Loading JSON will always give us string keys, and we need integers to get the
    # enum members from fields.
    labeled = {fields(int(num)): table for num, table in json_tables.items()}

    # Build Table objects with the entries and weights for each field.
    enum_tables = {}
    for label, inner_table in labeled.items():
        enum_tables[label] = tables.Table(
            inner_table['entries'],
            inner_table['weights'])

    return enum_tables


def build_item_tables(json_filename, fields):
    """
    Build item tables from a text file.

    The text file contains entries from a dice roll table in the following format:
    [number or number range] [item type]
    Example:
    42-46 Hammer
    """
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


def number_to_weight(number_string):
    """
    Returns 1 if number_string is a single number, or high end - low end + 1 if
    number_string is a range.
    """
    if "-" in number_string:
        number_range = number_string.split("-")
        low = int(number_range[0])
        high = int(number_range[1])
        weight = high - low + 1
    else:
        weight = 1

    return weight
