"""
File: exceptions.py
Author: Sean Reilly
Description: Defines exceptions used by the rest of the application
"""

class FilterParseException(Exception):
    """Raised if the filter parser cannot successfully parse the $filter query param"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class OrderByException(Exception):
    """Raised if there's a problem with the $orderby query param"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)