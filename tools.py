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


def build_item_tables(json_filename, item_filenames, fields):
    """
    Build item tables from a list of multiple text files (one text file per item
    subtype), then save the resulting tables as JSON using the provided filename.

    The text files contain entries from a dice roll table in the following format:
    [number or number range] [item type]
    Example:
    42-46 Hammer
    """
    # Build each table, adding it to a containing dictionary with an appropriate key.
    enum_tables = {table_name: tables.Table() for table_name in fields}

    # Because enum_tables and item_filenames were both built from an enum, they have
    # a predictable, repeatable order. That means we can match them up with zip().
    for item_table, item_file in zip(enum_tables.values(), item_filenames):
        try:
            with open(item_file, "r") as file:
                for line in file:
                    cleaned_line = line.strip()
                    # Split the entries into a number (or number range) and an item.
                    entry = cleaned_line.split(" ")
                    # Get the weight for this set of entries.
                    # For ranges, weight = top - bottom + 1. For single numbers,
                    # weight = 1.
                    weight = number_to_weight(entry[0])
                    # Get the specific item.
                    item = entry[1]

                    item_table.entries.append(item)
                    item_table.weights.append(weight)

        except FileNotFoundError:
            raise FileNotFoundError("No text file named {}!".format(item_file))

    # Save the resulting object to a JSON file for later use.
    save_tables(enum_tables, json_filename)


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
