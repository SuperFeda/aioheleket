class HeleketServerError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class HeleketValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class HeleketError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
