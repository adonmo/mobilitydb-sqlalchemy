import datetime
import pandas as pd
import pytest
from sqlalchemy.exc import StatementError

from .models import TemporalFloats


def test_simple_insert(session):
    df = pd.DataFrame(
        [
            {"value": 0, "t": datetime.datetime(2018, 1, 1, 12, 0, 0)},
            {"value": 8.2, "t": datetime.datetime(2018, 1, 1, 12, 6, 0)},
            {"value": 6.6, "t": datetime.datetime(2018, 1, 1, 12, 10, 0)},
            {"value": 9.1, "t": datetime.datetime(2018, 1, 1, 12, 15, 0)},
        ]
    ).set_index("t")

    session.add(TemporalFloats(tdata=df,))
    session.commit()

    sql = session.query(TemporalFloats).filter(TemporalFloats.id == 1)
    assert sql.count() == 1

    results = sql.all()
    for result in results:
        assert result.id == 1
        assert result.tdata.size == 4
        assert result.tdata.iloc[0].value == 0
        assert result.tdata.iloc[1].value == 8.2
        assert result.tdata.iloc[2].value == 6.6
        assert result.tdata.iloc[3].value == 9.1


def test_int_values_are_valid(session):
    df = pd.DataFrame(
        [
            {"value": 0, "t": datetime.datetime(2018, 1, 1, 12, 0, 0)},
            {"value": 8, "t": datetime.datetime(2018, 1, 1, 12, 6, 0)},
        ]
    ).set_index("t")

    session.add(TemporalFloats(tdata=df,))
    session.commit()


def test_bool_values_are_invalid(session):
    df = pd.DataFrame(
        [
            {"value": 0, "t": datetime.datetime(2018, 1, 1, 12, 0, 0)},
            {"value": True, "t": datetime.datetime(2018, 1, 1, 12, 6, 0)},
        ]
    ).set_index("t")

    with pytest.raises(StatementError):
        session.add(TemporalFloats(tdata=df,))
        session.commit()


def test_str_values_are_invalid(session):
    df = pd.DataFrame(
        [
            {"value": 0, "t": datetime.datetime(2018, 1, 1, 12, 0, 0)},
            {"value": "8", "t": datetime.datetime(2018, 1, 1, 12, 6, 0)},
        ]
    ).set_index("t")

    with pytest.raises(StatementError):
        session.add(TemporalFloats(tdata=df,))
        session.commit()
