class DatabaseError(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class ValidationError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
