import sqlalchemy.types as types


class Geometry(types.UserDefinedType):
    def get_col_spec(self, **kw):
        return "GEOMETRY"


class Geography(types.UserDefinedType):
    def get_col_spec(self, **kw):
        return "GEOGRAPHY"
