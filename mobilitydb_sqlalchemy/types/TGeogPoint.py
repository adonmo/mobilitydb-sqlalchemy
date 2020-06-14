from .TBaseGeomPoint import TBaseGeomPoint


class TGeogPoint(TBaseGeomPoint):
    def get_col_spec(self):
        return "TGEOGPOINT"
