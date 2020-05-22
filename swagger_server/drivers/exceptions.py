class SchemaError(Exception):
    pass


class SchemaExistedError(SchemaError):
    pass


class SchemaDoesNotExistError(SchemaError):
    pass


class UniqueConstraintViolationError(SchemaError):
    pass
