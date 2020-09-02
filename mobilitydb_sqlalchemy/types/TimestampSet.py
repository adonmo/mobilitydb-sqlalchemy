from pymeos.time import TimestampSet as MEOSTimestampSet
from sqlalchemy.types import UserDefinedType

from .BaseType import BaseType


class TimestampSet(BaseType):
    base_class = MEOSTimestampSet

    def get_col_spec(self):
        return "TIMESTAMPSET"
