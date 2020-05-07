import pandas as pd

from pymeos import DeserializerBool, SerializerBool, TInstantBool, TSequenceBool
from sqlalchemy.types import UserDefinedType

from .TBaseType import TBaseType


class TBool(TBaseType):
    pymeos_sequence_type = TSequenceBool
    pymeos_instant_type = TInstantBool
    pymeos_deserializer_type = DeserializerBool
    pymeos_serializer_type = SerializerBool

    def get_col_spec(self):
        return "TBOOL"

    @staticmethod
    def validate_type(value):
        dtype_kind = value["value"].dtypes.kind
        if not dtype_kind == "b":
            raise TypeError(
                "TBool needs bool values. Got: {} Expected {}".format(dtype_kind, "b")
            )
