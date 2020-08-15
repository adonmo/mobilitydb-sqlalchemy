import pandas as pd

from pymeos.temporal import TText
from pymeos.time import Period as MEOSPeriod
from sqlalchemy.types import UserDefinedType

from .TBaseType import TBaseType

def period_ident(self,t):
    return(t)

class Period(UserDefinedType):
    pymeos_instant_type = TText
    pymeos_deserializer_type = period_ident

    def get_col_spec(self):
        return "PERIOD"

    @staticmethod
    def validate_type(value):
        if not str(value):
            raise TypeError(
                "Period needs well-formatted string Got: {} Expected {}".format("??", "?")
            )

    def bind_processor(self, dialect):
        def process(value):
            self.validate_type(value)
            return(value)
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return MEOSPeriod(value)
        return process
