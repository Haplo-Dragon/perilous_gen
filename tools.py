import json


def build_tables(json_filename, fields):
    """
    Build tables from a text file, sorting each entry into categories based on fields.

    The text file contains the entries from a dice roll table in the following format:
    [number] [entry for field 1] [entry for field 2] [entry for field 3] etc.
    Example:
    42 Globe History Gyrating I- -kang
    """
    # Each field will get its own blank table.
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
