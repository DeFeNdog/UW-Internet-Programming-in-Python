"""
Module contains utility functions
"""


class Utilities():

    @staticmethod
    def format_currency_str(amount):
        return "${0:.2f}".format(float(amount))
