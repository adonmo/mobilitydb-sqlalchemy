from sqlalchemy.types import UserDefinedType


class BaseType(UserDefinedType):
    @property
    def base_class(self):
        raise NotImplementedError()

    @classmethod
    def validate_type(cls, value):
        if not isinstance(value, cls.base_class):
            raise TypeError(
                "Expected: {} Got: {} {}".format(cls.base_class, value.__class__, value)
            )

    def bind_processor(self, dialect):
        def process(value):
            self.validate_type(value)
            return str(value)

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return self.base_class(value)

        return process
