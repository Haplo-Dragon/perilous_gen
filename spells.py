from enum import Enum
import generator as gen
import os
import random
import templates


# Categories for the spell name random tables.
class Spell_Tables(Enum):
    FORM = 1
    NOUN = 2
    ADJECTIVE = 3
    WIZARD_NAME_PRE = 4
    WIZARD_NAME_POST = 5


# Templates matching fields for random tables with strings representing the names
# of spells, as in "Rincewind's Mighty Bolt".
SPELL_NAME_TEMPLATES = [
    # {noun} {form}
    templates.NameTemplate(
        [Spell_Tables.NOUN, Spell_Tables.FORM],
        "{} {}"),

    # {adjective} {form}
    templates.NameTemplate(
        [Spell_Tables.ADJECTIVE, Spell_Tables.FORM],
        "{} {}"),

    # {adjective} {noun}
    templates.NameTemplate(
        [Spell_Tables.ADJECTIVE, Spell_Tables.NOUN],
        "{} {}"),

    # {form} of {noun}
    templates.NameTemplate(
        [Spell_Tables.FORM, Spell_Tables.NOUN],
        "{} of {}"),

    # {form} of {adjective} {noun}
    templates.NameTemplate(
        [Spell_Tables.FORM, Spell_Tables.ADJECTIVE, Spell_Tables.NOUN],
        "{} of {} {}"),

    # {wizard name}'s {adjective} {form}'
    templates.NameTemplate(
        [Spell_Tables.WIZARD_NAME_PRE,
         Spell_Tables.WIZARD_NAME_POST,
         Spell_Tables.ADJECTIVE,
         Spell_Tables.FORM,
         ],
        "{}'s {} {}"),

    # {wizard name}'s {adjective} {noun}'
    templates.NameTemplate(
        [Spell_Tables.WIZARD_NAME_PRE,
         Spell_Tables.WIZARD_NAME_POST,
         Spell_Tables.ADJECTIVE,
         Spell_Tables.NOUN,
         ],
        "{}'s {} {}"),

    # {wizard name}'s {form} of {noun}'
    templates.NameTemplate(
        [Spell_Tables.WIZARD_NAME_PRE,
         Spell_Tables.WIZARD_NAME_POST,
         Spell_Tables.FORM,
         Spell_Tables.NOUN,
         ],
        "{}'s {} of {}"),

    # {wizard name}'s {noun} {form}'
    templates.NameTemplate(
        [Spell_Tables.WIZARD_NAME_PRE,
         Spell_Tables.WIZARD_NAME_POST,
         Spell_Tables.NOUN,
         Spell_Tables.FORM,
         ],
        "{}'s {} {}"),
]

# Some templates are more likely to be selected than others.
SPELL_NAME_TEMPLATE_WEIGHTS = [2, 2, 2, 1, 1, 1, 1, 1, 1]


class Spell_Generator(gen.PerilGenerator):
    """
    Generates random spell names using Jason Lute's 'Dungeons Monsters Treasure'.
    """

    def __init__(self):
        self.filename = os.path.join("tables", "Spells.json")
        gen.PerilGenerator.__init__(self, self.filename, Spell_Tables)

    def spell(self):
        """
        Generates a new random spell name.
        """
        # Using random.choices() allows us to specify weighting. We only need 1
        # result, so k=1, and we'll just take the first element of the (length 1)
        # list it returns.
        spell_name_template = random.choices(
            SPELL_NAME_TEMPLATES,
            SPELL_NAME_TEMPLATE_WEIGHTS,
            k=1)[0]

        spell_info = []
        wizard_name = None

        # Get a random entry for each category in the spell name template.
        for table in spell_name_template.fields:
            # Wizard names are split into prefixes and suffixes across two
            # tables, so when the prefix table comes up, we'll generate
            # the whole name, then skip the suffix when it comes up next (since
            # we don't want to accidentally generate two wizard names).
            if self.is_wizard_name(table, Spell_Tables):
                if wizard_name is None:
                    wizard_name = self.generate_wizard_name(Spell_Tables)
                    spell_info.append(wizard_name)
            else:
                feature = self.tables[table][random.randint(1, 100)]
                spell_info.append(feature)

        name_string = spell_name_template.string

        # We have to unpack the spell info list for this string formatting to work.
        spell_name = name_string.format(*spell_info)
        return spell_name
