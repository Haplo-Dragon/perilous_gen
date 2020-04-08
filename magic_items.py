from enum import Enum
import generator as gen
import os
import random
import spells
import tools


# General types of magic items.
class M_Item(Enum):
    SCROLL = 1
    POTION = 2
    GARB = 3
    JEWELRY = 4
    WAND = 5
    WEAPON = 6
    ARMOR = 7
    MISC = 8


# Categories for the magic item name random tables.
class M_ItemName(Enum):
    ITEM = 1
    NOUN = 2
    ADJECTIVE = 3
    WIZARD_NAME_PRE = 4
    WIZARD_NAME_POST = 5


# Strings representing the name of a magic item, as in "Rincewind's Smart Luggage".
M_ITEM_NAME_STRINGS = {
    # {noun} {item}
    1: "{} {}",
    # {adjective} {item}
    2: "{} {}",
    # {item} of the {noun}
    3: "{} of (the) {}",
    # {adjective} {item} of the {noun}
    4: "{} {} of the {}",
    # {wizard name}'s {item}
    5: "{}'s {}",
    # {wizard name}'s {item} of (the) {noun}
    6: "{}'s {} of (the) {}",
    # {wizard name}'s {adjective} {item}
    7: "{}'s {} {}",
    # {wizard name}'s {noun} {item}
    8: "{}'s {} {}",
}

M_ITEM_TEMPLATES = {
    # Each template matches up with a magic item name string above.
    1: [M_ItemName.NOUN, M_ItemName.ITEM],
    2: [M_ItemName.ADJECTIVE, M_ItemName.ITEM],
    3: [M_ItemName.ITEM, M_ItemName.NOUN],
    4: [M_ItemName.ADJECTIVE, M_ItemName.ITEM, M_ItemName.NOUN],
    5: [M_ItemName.WIZARD_NAME_PRE, M_ItemName.WIZARD_NAME_POST, M_ItemName.ITEM],
    6: [M_ItemName.WIZARD_NAME_PRE, M_ItemName.WIZARD_NAME_POST,
        M_ItemName.ITEM, M_ItemName.NOUN],
    7: [M_ItemName.WIZARD_NAME_PRE, M_ItemName.WIZARD_NAME_POST,
        M_ItemName.ADJECTIVE, M_ItemName.ITEM],
    8: [M_ItemName.WIZARD_NAME_PRE, M_ItemName.WIZARD_NAME_POST,
        M_ItemName.NOUN, M_ItemName.ITEM],
}


class M_Item_Generator(gen.PerilGenerator):
    """
    Generates random magic item names using Jason Lute's 'Dungeons Monsters Treasure'.
    """

    def __init__(self):
        self.filename = os.path.join("tables", "MagicItems.json")
        gen.PerilGenerator.__init__(self, self.filename, M_ItemName)
        self.init_item_types()

    def init_item_types(self):
        self.item_types = {
            1: M_Item.SCROLL,
            2: M_Item.POTION,
            3: M_Item.GARB,
            4: M_Item.JEWELRY,
            5: M_Item.WAND,
            6: M_Item.WEAPON,
            7: M_Item.ARMOR,
            8: M_Item.MISC,
        }
        self.item_type_filename = os.path.join("tables", "MagicItemTypes.json")
        try:
            self.item_tables = tools.load_tables(self.item_type_filename, M_Item)
        except FileNotFoundError:
            tools.build_item_tables(self.item_type_filename, M_Item)
            self.item_tables = tools.load_tables(self.item_type_filename, M_Item)

    def magic_item(self):
        """
        Generates a new random magic item.
        """
        # Get general item type.
        general_item_type = self.item_types[random.randint(1, len(self.item_types))]

        # A scroll will have a random spell inscribed on it.
        if general_item_type == M_Item.SCROLL:
            spell_gen = spells.Spell_Generator()
            spell_name = spell_gen.spell()
            return "Scroll of {}".format(spell_name)

        template = random.randint(1, 9)
        item_name_template = M_ITEM_TEMPLATES[template]

        item_info = []
        wizard_name = None

        # Get a random entry for each category in the item name template.
        for table in item_name_template:
            # Wizard names are split into prefixes and suffixes across two
            # tables, so when the prefix table comes up, we'll generate
            # the whole name, then skip the suffix when it comes up next (since
            # we don't want to accidentally generate two wizard names).
            if self.is_wizard_name(table, M_ItemName):
                if wizard_name is None:
                    wizard_name = self.generate_wizard_name(M_ItemName)
                    item_info.append(wizard_name)
            elif table == M_ItemName.ITEM:
                # Specific item (d100)
                item = self.generate_specific_item(general_item_type)
                item_info.append(item)
            else:
                feature = self.tables[table][random.randint(1, 100)]
                item_info.append(feature)

        name = M_ITEM_NAME_STRINGS[template]

        # # We have to unpack the item info list for this string formatting to work.
        item_name = name.format(*item_info)
        return item_name

    def generate_specific_item(self, general_item_type):
        raise NotImplementedError("Not done yet!")
