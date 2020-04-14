class NameTemplate:
    """
    A template for the name of an item or spell, consisting of fields for random tables
    and a string template to fill with results from those tables.
    """

    def __init__(self, fields, string):
        self.fields = fields
        self.string = string
