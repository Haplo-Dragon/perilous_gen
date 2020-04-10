import tools


class PerilGenerator:
    def __init__(self, table_file, table_fields):
        # First we'll try to load the tables from the specified JSON file.
        try:
            self.tables = tools.load_tables(table_file, table_fields)
        # If the JSON file doesn't exist, we'll try to build the tables from
        # a text file of the same name and save them to a JSON file for later
        # use.
        except FileNotFoundError:
            tools.build_tables(table_file, table_fields)
            self.tables = tools.load_tables(table_file, table_fields)

    def is_wizard_name(self, table, table_names):
        """
        Returns true if the given table is a wizard name table (prefix or suffix).
        """
        return (
            table == table_names.WIZARD_NAME_PRE or table == table_names.WIZARD_NAME_POST
        )

    def generate_wizard_name(self, table_names):
        """
        Generates a random wizard name.
        """
        # Get a random prefix and a random suffix.
        prefix = self.tables[table_names.WIZARD_NAME_PRE].random()
        suffix = self.tables[table_names.WIZARD_NAME_POST].random()

        # Join the prefix and suffix together after removing the hyphens.
        prefix = prefix.strip("-")
        suffix = suffix.strip("-")

        wizard = "".join([prefix, suffix])

        return wizard
