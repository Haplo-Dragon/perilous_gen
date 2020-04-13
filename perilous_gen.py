import click
import magic_items
import spells


@click.group()
def gen():
    """
    Generate random magic items or spells using Jason Lutes'
    "Dungeons Monsters Treasure".
    """
    pass


@gen.command()
@click.argument("num_items", type=int, default=1)
def item(num_items):
    """
    Generate random magic items.

    NUM_ITEMS is the number of magic items to generate.
    """
    click.echo("Generating {} random item(s)...".format(num_items))
    item_gen = magic_items.M_Item_Generator()
    for i in range(num_items):
        click.echo(item_gen.magic_item())


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
