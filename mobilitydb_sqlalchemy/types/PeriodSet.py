from pymeos.time import PeriodSet as MEOSPeriodSet
from sqlalchemy.types import UserDefinedType

from .BaseType import BaseType


class PeriodSet(BaseType):
    base_class = MEOSPeriodSet

    def get_col_spec(self):
        return "PERIODSET"
