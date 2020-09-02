from pymeos.time import Period as MEOSPeriod
from sqlalchemy.types import UserDefinedType


class Period(UserDefinedType):
    def get_col_spec(self):
        return "PERIOD"

    @staticmethod
    def validate_type(value):
        if not isinstance(value, MEOSPeriod):
            raise TypeError(
                "Period needs to be of type {} Got: {} {}".format(
                    MEOSPeriod, value.__class__, value
                )
            )

    def bind_processor(self, dialect):
        def process(value):
            self.validate_type(value)
            return str(value)

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return MEOSPeriod(value)

        return process
