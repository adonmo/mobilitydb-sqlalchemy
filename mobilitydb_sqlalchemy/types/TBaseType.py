import pandas as pd

from sqlalchemy.types import UserDefinedType

from mobilitydb_sqlalchemy.comparator import Comparator


class TBaseType(UserDefinedType):
    """
    TBaseType is a wrapper around UserDefinedType on top of which mobilitydb's
    temporal types can be defined. It uses pandas DataFrames to provide structure
    for the common temporal nature of these types.

    Children of this class are expected to implement the functions `validate_type`,
    `write_instant_value`, `parse_instant_value` and the properties `pymeos_*_type`
    must be set accordingly.
    """

    pandas_value_column = "value"
    comparator_factory = Comparator

    @property
    def pymeos_sequence_type(self):
        raise NotImplementedError()

    @property
    def pymeos_instant_type(self):
        raise NotImplementedError()

    @property
    def pymeos_deserializer_type(self):
        raise NotImplementedError()

    @staticmethod
    def validate_type(value):
        raise NotImplementedError()

    @staticmethod
    def write_instant_value(value):
        return value

    @staticmethod
    def parse_instant_value(value):
        return value

    def __init__(self, left_closed=True, right_closed=True):
        self.left_closed = left_closed
        self.right_closed = right_closed

    def bind_processor(self, dialect):
        def process(value):
            self.validate_type(value)
            value.sort_index(inplace=True)

            instants = {
                self.pymeos_instant_type(
                    self.write_instant_value(
                        getattr(value.loc[v], self.pandas_value_column)
                    ),
                    v,
                )
                for v in value.index
            }
            sequence = self.pymeos_sequence_type(
                instants, self.left_closed, self.right_closed
            )
            return str(sequence)

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            tseq = self.pymeos_deserializer_type(value).nextTSequence()
            df = pd.DataFrame(
                [
                    {
                        self.pandas_value_column: self.parse_instant_value(i.getValue),
                        "t": i.getTimestamp,
                    }
                    for i in sorted(tseq.instants)
                ]
            )
            df["t"] = pd.to_datetime(df["t"])
            df.set_index("t", inplace=True)
            return df

        return process
