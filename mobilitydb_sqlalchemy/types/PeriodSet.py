from pymeos.time import PeriodSet as MEOSPeriodSet
from sqlalchemy.types import UserDefinedType


class PeriodSet(UserDefinedType):
    def get_col_spec(self):
        return "PERIODSET"

    @staticmethod
    def validate_type(value):
        if not isinstance(value, MEOSPeriodSet):
            raise TypeError(
                "PeriodSet needs to be of type {} Got: {} {}".format(
                    MEOSPeriodSet, value.__class__, value
                )
            )

    def bind_processor(self, dialect):
        def process(value):
            self.validate_type(value)
            return str(value)

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return MEOSPeriodSet(value)

        return process
