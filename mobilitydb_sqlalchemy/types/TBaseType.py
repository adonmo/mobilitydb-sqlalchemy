import pandas as pd

from sqlalchemy.types import UserDefinedType
from mobilitydb_sqlalchemy.comparator import Comparator


class TBaseType(UserDefinedType):
    """
    TBaseType is a wrapper around UserDefinedType on top of which mobilitydb's
    temporal types can be defined. It uses pandas DataFrames to provide structure
    for the common temporal nature of these types.

    Children of this class are expected to implement the functions `validate_type`,
    `write_instant_value` and `parse_instant_value`.
    """

    pandas_value_column = "value"
    comparator_factory = Comparator

    @staticmethod
    def validate_type(value):
        raise NotImplementedError()

    @staticmethod
    def write_instant_value(value):
        raise NotImplementedError()

    @staticmethod
    def parse_instant_value(value):
        raise NotImplementedError()

    def __init__(self, left_closed=True, right_closed=True):
        self.left_closed = left_closed
        self.right_closed = right_closed

    def bind_processor(self, dialect):
        def process(value):
            self.validate_type(value)
            value.sort_index(inplace=True)
            instants = list(value.loc[v] for v in value.index)
            left_bound = "[" if self.left_closed else "("
            right_bound = "]" if self.right_closed else ")"
            return "{}{}{}".format(
                left_bound,
                ", ".join(
                    "{}@{}".format(
                        self.write_instant_value(getattr(i, self.pandas_value_column)),
                        i.name,
                    )
                    for i in instants
                ),
                right_bound,
            )

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            instants = [i.strip().split("@") for i in value[1:-1].split(",")]
            df = pd.DataFrame(
                [
                    {
                        self.pandas_value_column: self.parse_instant_value(i[0]),
                        "t": i[1],
                    }
                    for i in instants
                ]
            )
            df["t"] = pd.to_datetime(df["t"])
            df.set_index("t", inplace=True)
            return df

        return process
