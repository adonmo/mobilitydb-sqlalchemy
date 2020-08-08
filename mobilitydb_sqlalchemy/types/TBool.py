import pandas as pd

from pymeos.io import DeserializerBool
from pymeos.temporal import TBoolInst, TBoolSeq
from sqlalchemy.types import UserDefinedType

from .TBaseType import TBaseType


class TBool(TBaseType):
    pymeos_sequence_type = TBoolSeq
    pymeos_instant_type = TBoolInst
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
