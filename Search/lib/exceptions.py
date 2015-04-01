

class PurchaseException(Exception):
    def __init__(self, message):
        self.message = message

        # Call the base class constructor with the parameters it needs
        super(PurchaseException, self).__init__(message)


class OfferException(Exception):
    def __init__(self, message):
        self.message = message

        # Call the base class constructor with the parameters it needs
        super(OfferException, self).__init__(message)