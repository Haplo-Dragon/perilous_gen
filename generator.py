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
