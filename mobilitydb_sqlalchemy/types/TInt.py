import pandas as pd

from pymeos.io import DeserializerInt
from pymeos.temporal import TInstantInt, TSequenceInt
from sqlalchemy.types import UserDefinedType

from .TBaseType import TBaseType


class TInt(TBaseType):
    pymeos_sequence_type = TSequenceInt
    pymeos_instant_type = TInstantInt
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
