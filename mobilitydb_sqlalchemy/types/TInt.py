import pandas as pd

from pymeos import DeserializerInt, SerializerInt, TInstantInt, TSequenceInt
from sqlalchemy.types import UserDefinedType

from .TBaseType import TBaseType


class TInt(TBaseType):
    pymeos_sequence_type = TSequenceInt
    pymeos_instant_type = TInstantInt
    pymeos_deserializer_type = DeserializerInt
    pymeos_serializer_type = SerializerInt

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
