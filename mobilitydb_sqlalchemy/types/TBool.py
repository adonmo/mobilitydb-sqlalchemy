import pandas as pd

from pymeos import DeserializerBool
from sqlalchemy.types import UserDefinedType

from .TBaseType import TBaseType


class TBool(TBaseType):
    pymeos_deserializer_type = DeserializerBool

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
