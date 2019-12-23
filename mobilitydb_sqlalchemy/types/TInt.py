import pandas as pd

from sqlalchemy.types import UserDefinedType

from .TBaseType import TBaseType


class TInt(TBaseType):
    def get_col_spec(self):
        return "TINT"

    @staticmethod
    def validate_type(value):
        dtype_kind = value["value"].dtypes.kind
        if not dtype_kind == "i":
            raise TypeError(
                "TInt needs int values. Got: {} Expected {}".format(dtype_kind, "i")
            )

    @staticmethod
    def write_instant_value(value):
        return str(value)

    @staticmethod
    def parse_instant_value(value):
        return int(value)
