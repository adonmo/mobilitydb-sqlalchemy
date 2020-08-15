import re

import pandas as pd
from pymeos import GeomPoint
from pymeos.io import DeserializerGeom
from pymeos.temporal import TGeomPointInst, TGeomPointSeq
from shapely.geometry import Point
from shapely.wkt import loads
from sqlalchemy import func
from sqlalchemy.types import UserDefinedType

from .TBaseType import TBaseType

try:
    import movingpandas as mpd
    from fiona.crs import from_epsg
    from geopandas import GeoDataFrame

    MOVING_PANDAS = True
    CRS_METRIC = from_epsg(31256)
except ImportError:
    MOVING_PANDAS = False


class TBaseGeomPoint(TBaseType):
    pymeos_sequence_type = TGeomPointSeq
    pymeos_instant_type = TGeomPointInst
    pymeos_deserializer_type = DeserializerGeom

    # This is ensure compatibility with movingpandas
    pandas_value_column = "geometry"

    def __init__(self, left_closed=True, right_closed=True, use_movingpandas=False):
        super().__init__(left_closed=left_closed, right_closed=right_closed)
        self.use_movingpandas = use_movingpandas

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
        return GeomPoint(value.wkt)

    @staticmethod
    def parse_instant_value(value):
        point = loads(value.toWKT())
        if type(point) != Point:
            raise TypeError("Expected Point, got: " + type(point))
        return point

    def bind_processor(self, dialect):
        parent_process = super().bind_processor(dialect)
        use_movingpandas = self.use_movingpandas

        def process(value):
            if use_movingpandas:
                if MOVING_PANDAS:
                    return parent_process(value.df)
                else:
                    raise ModuleNotFoundError(
                        "movingpandas is optional dependency. Add it using pip install movingpandas"
                    )
            return parent_process(value)

        return process

    def result_processor(self, dialect, coltype):
        parent_process = super().result_processor(dialect, coltype)
        use_movingpandas = self.use_movingpandas

        def process(value):
            df = parent_process(value)
            if use_movingpandas:
                if MOVING_PANDAS:
                    geo_df = GeoDataFrame(df, crs=CRS_METRIC)
                    traj = mpd.Trajectory(geo_df, 1)
                    return traj
                else:
                    raise ModuleNotFoundError(
                        "movingpandas is optional dependency. Add it using pip install movingpandas"
                    )
            return df

        return process
