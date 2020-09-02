from pymeos.box import TBox as MEOSTBox
from sqlalchemy.types import UserDefinedType

from .BaseType import BaseType


class TBox(BaseType):
    base_class = MEOSTBox

    def get_col_spec(self):
        return "TBOX"
