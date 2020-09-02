from pymeos.range import RangeInt as MEOSRangeInt
from sqlalchemy.types import UserDefinedType

from .BaseType import BaseType


class RangeInt(BaseType):
    base_class = MEOSRangeInt

    def get_col_spec(self):
        return "INTRANGE"
