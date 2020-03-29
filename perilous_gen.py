from enum import Enum
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


class Spell:
    def __init__(self):
        # self.noun = None
        # self.form = None
        # self.adjective = None
        # self.wizard_name = None
        # self.name_template = None
        self.tables = build_tables("SpellNames.txt")
        self.wizard_name = None
        self.generate_name()

    def generate_name(self):
        template = random.randint(1, 9)

        spell_name_template = SPELL_NAME_TEMPLATES[template]
        spell_info = []

        for table in spell_name_template:
            if self.is_wizard_name(table):
                if self.wizard_name is None:
                    spell_info.append(self.generate_wizard_name())
            else:
                feature = self.tables[table][random.randint(1, 100)]
                spell_info.append(feature)

        name = SPELL_NAME_STRINGS[template]

        # We have to unpack the spell info list for this string formatting to work.
        self.name = name.format(*spell_info)

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
        self.wizard_name = wizard

        return wizard

    def __str__(self):
        return str(self.name)


def build_tables(filename):
    tables = {table_name: {} for table_name in Spell_Tables}

    with open(filename, "r") as file:
        for line in file:
            cleaned_line = line.strip()
            entry = cleaned_line.split(" ")
            number = int(entry[0])

            for table, item in zip(tables.values(), entry[1:]):
                table[number] = item

    return tables


if __name__ == "__main__":
    num_spells = int(sys.argv[1])

    for i in range(num_spells):
        spell = Spell()
        print(spell)
