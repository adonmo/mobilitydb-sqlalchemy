import pandas as pd

from pymeos.io import DeserializerInt
from pymeos.temporal import TIntInst, TIntSeq
from sqlalchemy.types import UserDefinedType

from .TBaseType import TBaseType


class TInt(TBaseType):
    pymeos_sequence_type = TIntSeq
    pymeos_instant_type = TIntInst
    pymeos_deserializer_type = DeserializerInt

    def get_col_spec(self):
        return "TINT"

    @staticmethod
    def validate_type(value):
        dtype_kind = value["value"].dtypes.kind
        if not dtype_kind == "i":
            raise TypeError(
                "TInt needs int values. Got: {} Expected {}".format(dtype_kind, "i")
            )
