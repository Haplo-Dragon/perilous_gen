import spells
import sys


if __name__ == "__main__":
    if len(sys.argv) > 1:
        num_spells = int(sys.argv[1])
    else:
        num_spells = 1

    spell_gen = spells.Spell_Generator()
    for i in range(num_spells):
        print(spell_gen.spell())
