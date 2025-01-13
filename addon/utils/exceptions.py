# ==================================================================
# addon/components/exceptions.py
# ==================================================================
# TODO
# Not implemented yet
# ==================================================================

class CardNotFoundError(Exception):
    """
    Raised when a card operation fails because the card cannot be found.
    """

    pass


class CardOperationError(Exception):
    """
    Raised when a card operation fails for any other reason.
    """

    pass
