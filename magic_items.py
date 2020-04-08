from enum import Enum
import generator as gen
import random

# General item type (d12)
# Specific item (d100)
# Item name template
# Item name


# Categories for the magic item random tables.
class M_Item(Enum):
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
    3: "{} of the {}",
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
    1: [M_Item.NOUN, M_Item.ITEM],
    2: [M_Item.ADJECTIVE, M_Item.ITEM],
    3: [M_Item.ITEM, M_Item.NOUN],
    4: [M_Item.ADJECTIVE, M_Item.ITEM, M_Item.NOUN],
    5: [M_Item.WIZARD_NAME_PRE, M_Item.WIZARD_NAME_POST, M_Item.ITEM],
    6: [M_Item.WIZARD_NAME_PRE, M_Item.WIZARD_NAME_POST, M_Item.ITEM, M_Item.NOUN],
    7: [M_Item.WIZARD_NAME_PRE, M_Item.WIZARD_NAME_POST, M_Item.ADJECTIVE, M_Item.ITEM],
    8: [M_Item.WIZARD_NAME_PRE, M_Item.WIZARD_NAME_POST, M_Item.NOUN, M_Item.ITEM],
}


class M_Item_Generator(gen.PerilGenerator):
    """
    Generates random magic item names using Jason Lute's 'Dungeons Monsters Treasure'.
    """

    def __init__(self):
        gen.PerilGenerator.__init__(self, "MagicItems.json", M_Item)
