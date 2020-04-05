from enum import Enum
import generator as gen
import random
import tools


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


class Spell_Generator(gen.PerilGenerator):
    def __init__(self):
        # try:
        #     self.tables = tools.load_tables("Spells.json", Spell_Tables)
        # except FileNotFoundError:
        #     # If the JSON tables don't exist yet, we'll create them from a text file.
        #     tools.build_tables("Spells.json", Spell_Tables)
        #     self.tables = tools.load_tables("Spells.json", Spell_Tables)
        gen.PerilGenerator.__init__(self, "Spells.json", Spell_Tables)

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
