from .TBaseGeomPoint import TBaseGeomPoint


class TGeomPoint(TBaseGeomPoint):
    def get_col_spec(self):
        return "TGEOMPOINT"
