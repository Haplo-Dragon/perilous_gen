import random


class Table:
    """
    A table holding entries to be chosen randomly with weighted probabilities.
    """

    def __init__(self, entries=None, weights=None):
        self.entries = [] if entries is None else entries
        self.weights = [] if weights is None else weights

    def random(self):
        """
        Returns a random item from the table.
        """
        # Using random.choices() allows us to specify weighting. We only need 1
        # result, so k=1, and we'll just take the first element of the (length 1)
        # list it returns.
        return random.choices(self.entries, self.weights, k=1)[0]
