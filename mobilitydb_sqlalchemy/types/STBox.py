from pymeos.box import STBox as MEOSSTBox
from sqlalchemy.types import UserDefinedType

from .BaseType import BaseType


class STBox(BaseType):
    base_class = MEOSSTBox

    def get_col_spec(self):
        return "STBOX"
