from pymeos.range import RangeFloat as MEOSRangeFloat
from sqlalchemy.types import UserDefinedType

from .BaseType import BaseType


class RangeFloat(BaseType):
    base_class = MEOSRangeFloat

    def get_col_spec(self):
        return "FLOATRANGE"
