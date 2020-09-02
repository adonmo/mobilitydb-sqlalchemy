from pymeos.time import Period as MEOSPeriod
from sqlalchemy.types import UserDefinedType

from .BaseType import BaseType


class Period(BaseType):
    base_class = MEOSPeriod

    def get_col_spec(self):
        return "PERIOD"
