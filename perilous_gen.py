from enum import Enum
import json
import random
import sys


class Spell_Tables(Enum):
    FORM = 1
    NOUN = 2
    ADJECTIVE = 3
    WIZARD_NAME_PRE = 4
    WIZARD_NAME_POST = 5


SPELL_NAME_STRINGS = {
    # {noun} {form}
    1: "{} {}",
    # {adjective} {form}
    2: "{} {}",
    # {adjective} {noun}
    3: "{} {}",
    # {form} of {noun}
    4: "{} of {}",
    # {form} of {adjective} {noun}
    5: "{} of {} {}",
    # {wizard name}'s {adjective} {form}'
    6: "{}'s {} {}",
    # {wizard name}'s {adjective} {noun}'
    7: "{}'s {} {}",
    # {wizard name}'s {form} of {noun}'
    8: "{}'s {} of {}",
    # {wizard name}'s {noun} {form}'
    9: "{}'s {} {}",
}

SPELL_NAME_TEMPLATES = {
    1: [Spell_Tables.NOUN, Spell_Tables.FORM],
    2: [Spell_Tables.ADJECTIVE, Spell_Tables.FORM],
    3: [Spell_Tables.ADJECTIVE, Spell_Tables.NOUN],
    4: [Spell_Tables.FORM, Spell_Tables.NOUN],
    5: [Spell_Tables.FORM, Spell_Tables.ADJECTIVE, Spell_Tables.NOUN],
    6: [
        Spell_Tables.WIZARD_NAME_PRE,
        Spell_Tables.WIZARD_NAME_POST,
        Spell_Tables.ADJECTIVE,
        Spell_Tables.FORM,
    ],
    7: [
        Spell_Tables.WIZARD_NAME_PRE,
        Spell_Tables.WIZARD_NAME_POST,
        Spell_Tables.ADJECTIVE,
        Spell_Tables.NOUN,
    ],
    8: [
        Spell_Tables.WIZARD_NAME_PRE,
        Spell_Tables.WIZARD_NAME_POST,
        Spell_Tables.FORM,
        Spell_Tables.NOUN,
    ],
    9: [
        Spell_Tables.WIZARD_NAME_PRE,
        Spell_Tables.WIZARD_NAME_POST,
        Spell_Tables.NOUN,
        Spell_Tables.FORM,
    ],
}


class Spell_Generator:
    def __init__(self):
        try:
            self.tables = load_tables("Spells.json")
        except FileNotFoundError:
            # If the JSON tables don't exist yet, we'll create them from a text file.
            build_tables("Spells.json")
            self.tables = load_tables("Spells.json")

    def spell(self):
        template = random.randint(1, 9)

        spell_name_template = SPELL_NAME_TEMPLATES[template]
        spell_info = []
        wizard_name = None

        for table in spell_name_template:
            # print("Generating a {}.".format(table))
            if self.is_wizard_name(table):
                if wizard_name is None:
                    # print("\tGenerating name for first time.")
                    wizard_name = self.generate_wizard_name()
                    spell_info.append(wizard_name)
            else:
                feature = self.tables[table][random.randint(1, 100)]
                spell_info.append(feature)

        name = SPELL_NAME_STRINGS[template]

        # We have to unpack the spell info list for this string formatting to work.
        spell_name = name.format(*spell_info)
        return spell_name

    def is_wizard_name(self, table):
        return (
            table == Spell_Tables.WIZARD_NAME_PRE
            or table == Spell_Tables.WIZARD_NAME_POST
        )

    def generate_wizard_name(self):
        prefix = self.tables[Spell_Tables.WIZARD_NAME_PRE][random.randint(1, 100)]
        suffix = self.tables[Spell_Tables.WIZARD_NAME_POST][random.randint(1, 100)]
        prefix = prefix.strip("-")
        suffix = suffix.strip("-")

        wizard = "".join([prefix, suffix])

        return wizard

    def __str__(self):
        return str(self.name)


def build_tables(json_filename):
    tables = {table_name: {} for table_name in Spell_Tables}

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


def load_tables(filename):
    """
    Load tables from a JSON file, adjusting their keys to be integers.
    """
    try:
        with open(filename, "r") as file:
            json_tables = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("No JSON file named {}!".format(filename))

    # Loading JSON will always give us string keys, and we need integers.
    labeled = {Spell_Tables(int(num)): table for num, table in json_tables.items()}
    # The same is true for the inner tables.
    for key, inner_table in labeled.items():
        labeled[key] = {int(k): v for k, v in inner_table.items()}

    return labeled


if __name__ == "__main__":
    if len(sys.argv) > 1:
        num_spells = int(sys.argv[1])
    else:
        num_spells = 1

    spell_gen = Spell_Generator()
    for i in range(num_spells):
        print(spell_gen.spell())
