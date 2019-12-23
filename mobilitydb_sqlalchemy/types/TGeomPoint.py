import pandas as pd
import re
from shapely.geometry import Point
from shapely.wkt import loads
from sqlalchemy import func
from sqlalchemy.types import UserDefinedType

from .TBaseType import TBaseType


class TGeomPoint(TBaseType):
    # This is ensure compatibility with movingpandas
    pandas_value_column = "geometry"

    def get_col_spec(self):
        return "TGEOMPOINT"

    def column_expression(self, col):
        # TODO use func.asBinary, as probably that will be more efficient
        return func.asText(col, type_=self)

    @staticmethod
    def validate_type(value):
        # TODO validate Point type in the dataframe
        pass

    @staticmethod
    def write_instant_value(value):
        return value.wkt

    @staticmethod
    def parse_instant_value(value):
        point = loads(value)
        if type(point) != Point:
            raise TypeError("Expected Point, got: " + type(point))
        return point
