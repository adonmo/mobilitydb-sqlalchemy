import pandas as pd

from sqlalchemy.types import UserDefinedType
from pandas.api.types import is_numeric_dtype

from .TBaseType import TBaseType


class TFloat(TBaseType):
    def get_col_spec(self):
        return "TFLOAT"

    @staticmethod
    def validate_type(value):
        dtypes = value["value"].dtypes
        if not is_numeric_dtype(dtypes):
            raise TypeError(
                "TInt needs int values. Got: {} Expected {}".format(dtypes.kind, "f")
            )

    @staticmethod
    def write_instant_value(value):
        return str(value)

    @staticmethod
    def parse_instant_value(value):
        return float(value)
