import click
import magic_items
import spells

# RANDOM, SCROLL, POTION, GARB, JEWELRY, WAND, WEAPON, ARMOR, or MISC.
item_choices = [item.name for item in magic_items.M_Item]
item_choices.append("RANDOM")


@click.group()
def gen():
    """
    Generate random magic items or spells using Jason Lutes'
    "Dungeons Monsters Treasure".
    """
    pass


@gen.command()
@click.argument("num_items", type=int, default=1)
@click.option("-i", "--item",
              type=click.Choice(item_choices, case_sensitive=False),
              default="RANDOM")
def item(num_items, item):
    """
    Generate random magic items.

    NUM_ITEMS is the number of magic items to generate.
    """
    if item == "RANDOM":
        click.echo("Generating {} random item(s)...".format(num_items))
        random_item(num_items, item)
    else:
        click.echo("Generating {} random {}...".format(num_items, item.casefold()))
        specific_item(num_items, magic_items.M_Item[item])


def random_item(num_items, item):
    """
    Generate num_items random magic items.
    """
    item_gen = magic_items.M_Item_Generator()
    for i in range(num_items):
        click.echo(item_gen.magic_item())


def specific_item(num_items, item_type):
    """
    Generate num_items random magic items of the specified type.
    """
    item_gen = magic_items.M_Item_Generator()
    for i in range(num_items):
        click.echo(item_gen.specific_item(item_type))


@gen.command()
@click.argument("num_items", type=int, default=1)
def spell(num_items):
    """
    Generate random spells.

    NUM_ITEMS is the number of spells to generate.
    """
    click.echo("Generating {} random spell(s)...".format(num_items))
    spell_gen = spells.Spell_Generator()
    for i in range(num_items):
        click.echo(spell_gen.spell())


if __name__ == "__main__":
    gen()
