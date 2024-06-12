class FilterParseException(Exception):
    """Raised if the filter parser cannot successfully parse the $filter query param"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)