import json


def build_tables(json_filename, fields):
    tables = {table_name: {} for table_name in fields}

    # Strip the JSON extension from the filename and add a TXT extension.
    text_filename = json_filename[:-5]
    text_filename += ".txt"

    try:
        with open(text_filename, "r") as file:
            for line in file:
                cleaned_line = line.strip()
                entry = cleaned_line.split(" ")
                number = int(entry[0])

                for table, item in zip(tables.values(), entry[1:]):
                    table[number] = item
    except FileNotFoundError:
        raise FileNotFoundError(
            "Couldn't find a text file named {} with table data!".format(text_filename)
        )

    save_tables(tables, json_filename)


def save_tables(tables, filename):
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
    # The same is true for the inner tables.
    for key, inner_table in labeled.items():
        labeled[key] = {int(k): v for k, v in inner_table.items()}

    return labeled
