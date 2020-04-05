import tools


class PerilGenerator():
    def __init__(self, table_file, table_fields):
        try:
            self.tables = tools.load_tables(table_file, table_fields)
        except FileNotFoundError:
            tools.build_tables(table_file, table_fields)
            self.tables = tools.load_tables(table_file, table_fields)
