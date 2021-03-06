from enum import Enum
import generator as gen
import os
import spells
import tables
import templates
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


M_Item_Weights = [1, 3, 1, 2, 1, 1, 1, 2]


# Categories for the magic item name random tables.
class M_ItemName(Enum):
    ITEM = 1
    NOUN = 2
    ADJECTIVE = 3
    WIZARD_NAME_PRE = 4
    WIZARD_NAME_POST = 5


# Templates matching fields for random tables with strings representing the names
# of magic items, as in "Rincewind's Smart Luggage".
M_ITEM_TEMPLATES = [
    # {noun} {item}
    templates.NameTemplate(
        [M_ItemName.NOUN, M_ItemName.ITEM],
        "{} {}"),

    # {adjective} {item}
    templates.NameTemplate(
        [M_ItemName.ADJECTIVE, M_ItemName.ITEM],
        "{} {}"),

    # {item} of the {noun}
    templates.NameTemplate(
        [M_ItemName.ITEM, M_ItemName.NOUN],
        "{} of (the) {}"),

    # {adjective} {item} of the {noun}
    templates.NameTemplate(
        [M_ItemName.ADJECTIVE, M_ItemName.ITEM, M_ItemName.NOUN],
        "{} {} of the {}"),

    # {wizard name}'s {item}
    templates.NameTemplate(
        [M_ItemName.WIZARD_NAME_PRE, M_ItemName.WIZARD_NAME_POST, M_ItemName.ITEM],
        "{}'s {}"),

    # {wizard name}'s {item} of (the) {noun}
    templates.NameTemplate(
        [
            M_ItemName.WIZARD_NAME_PRE,
            M_ItemName.WIZARD_NAME_POST,
            M_ItemName.ITEM,
            M_ItemName.NOUN,
        ],
        "{}'s {} of (the) {}"),

    # {wizard name}'s {adjective} {item}
    templates.NameTemplate(
        [
            M_ItemName.WIZARD_NAME_PRE,
            M_ItemName.WIZARD_NAME_POST,
            M_ItemName.ADJECTIVE,
            M_ItemName.ITEM,
        ],
        "{}'s {} {}"),

    # {wizard name}'s {noun} {item}
    templates.NameTemplate(
        [
            M_ItemName.WIZARD_NAME_PRE,
            M_ItemName.WIZARD_NAME_POST,
            M_ItemName.NOUN,
            M_ItemName.ITEM,
        ],
        "{}'s {} {}"),
]

# Some templates are more likely to be selected than others.
M_ITEM_TEMPLATE_WEIGHTS = [2, 2, 2, 2, 1, 1, 1, 1]

M_ITEM_TEMPLATE_TABLE = tables.Table(M_ITEM_TEMPLATES, M_ITEM_TEMPLATE_WEIGHTS)


class M_Item_Generator(gen.PerilGenerator):
    """
    Generates random magic item names using Jason Lute's 'Dungeons Monsters Treasure'.
    """

    def __init__(self):
        self.filename = os.path.join("tables", "MagicItems.json")
        # magic_item_name_fields = [
        #     M_ItemName.NOUN,
        #     M_ItemName.ADJECTIVE,
        #     M_ItemName.WIZARD_NAME_PRE,
        #     M_ItemName.WIZARD_NAME_POST]

        # gen.PerilGenerator.__init__(self, self.filename, magic_item_name_fields)
        gen.PerilGenerator.__init__(self, self.filename, M_ItemName)

        self.item_types = tables.Table(list(M_Item), M_Item_Weights)
        self.items = self.init_item_tables()

    def init_item_tables(self):
        specific_items_filename = os.path.join("tables", "Items.json")

        try:
            items = tools.load_tables(specific_items_filename, M_Item)
        except FileNotFoundError:
            item_paths = self.build_item_filepaths()
            tools.build_item_tables(specific_items_filename, item_paths, M_Item)
            items = tools.load_tables(specific_items_filename, M_Item)

        return items

    def build_item_filepaths(self):
        """
        Returns a list of text filenames matching the members of M_Item.
        """
        item_paths = [item.name + ".txt" for item in M_Item]
        item_paths = [os.path.join("tables", item) for item in item_paths]

        return item_paths

    def magic_item(self):
        """
        Generates a new random magic item.
        """
        return self._random_item(self.item_types.random())

    def specific_item(self, general_item_type):
        """
        Generates a new random magic item of the specified type.
        """
        return self._random_item(general_item_type)

    def scroll(self):
        """
        Generates a new random magic scroll.
        """
        return self._scroll()

    def potion(self):
        """
        Generates a new random magic potion.
        """
        return self._random_item(M_Item.POTION)

    def garb(self):
        """
        Generates a new random piece of magic garb/clothing.
        """
        return self._random_item(M_Item.GARB)

    def jewelry(self):
        """
        Generates a new random piece of magic jewelry.
        """
        return self._random_item(M_Item.JEWELRY)

    def wand(self):
        """
        Generates a new random magic wand.
        """
        return self._random_item(M_Item.WAND)

    def weapon(self):
        """
        Generates a new random magic weapon.
        """
        return self._random_item(M_Item.WEAPON)

    def armor(self):
        """
        Generates a new random piece of magic armor.
        """
        return self._random_item(M_Item.ARMOR)

    def misc_item(self):
        """
        Generates a new random miscellaneous magic item.
        """
        return self._random_item(M_Item.MISC)

    def _random_item(self, general_item_type):
        """
        Generates a random magic item of general_item_type.
        """
        # A scroll will have a random spell inscribed on it.
        if general_item_type == M_Item.SCROLL:
            return self._scroll()

        item_name_template = M_ITEM_TEMPLATE_TABLE.random()

        item_info = []
        wizard_name = None

        # Get a random entry for each category in the item name template.
        for table in item_name_template.fields:
            # Wizard names are split into prefixes and suffixes across two
            # tables, so when the prefix table comes up, we'll generate
            # the whole name, then skip the suffix when it comes up next (since
            # we don't want to accidentally generate two wizard names).
            if self.is_wizard_name(table, M_ItemName):
                if wizard_name is None:
                    wizard_name = self.generate_wizard_name(M_ItemName)
                    item_info.append(wizard_name)

            elif table == M_ItemName.ITEM:
                item = self.generate_specific_item(general_item_type)
                item_info.append(item)

            else:
                feature = self.tables[table].random()
                item_info.append(feature)

        name_string = item_name_template.string

        # # We have to unpack the item info list for this string formatting to work.
        item_name = name_string.format(*item_info)
        return item_name

    def generate_specific_item(self, general_item_type):
        """
        Returns a randomly chosen specific item of general_item_type.
        """
        return self.items[general_item_type].random()

    def _scroll(self):
        """
        Generates a scroll with a random spell inscribed on it.
        """
        spell_gen = spells.Spell_Generator()
        spell_name = spell_gen.spell()
        return "Scroll of {}".format(spell_name)
