class SchemaError(Exception):
    pass


class SchemaExisted(SchemaError):
    pass


class SchemaDoesNotExist(SchemaError):
    pass


class UniqueConstraintViolation(SchemaError):
    pass
