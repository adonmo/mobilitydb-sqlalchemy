import pandas as pd

from sqlalchemy.types import UserDefinedType

from .TBaseType import TBaseType


class TBool(TBaseType):
    def get_col_spec(self):
        return "TBOOL"

    @staticmethod
    def validate_type(value):
        dtype_kind = value["value"].dtypes.kind
        if not dtype_kind == "b":
            raise TypeError(
                "TBool needs bool values. Got: {} Expected {}".format(dtype_kind, "b")
            )

    @staticmethod
    def write_instant_value(py_bool):
        return "t" if py_bool else "f"

    @staticmethod
    def parse_instant_value(valuez):
        return valuez == "t"
