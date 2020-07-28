import datetime
import pandas as pd
import pytest
from sqlalchemy.exc import StatementError

from .models import TemporalBools


def test_simple_insert(session):
    df = pd.DataFrame(
        [
            {"value": False, "t": datetime.datetime(2018, 1, 1, 12, 0, 0)},
            {"value": True, "t": datetime.datetime(2018, 1, 1, 12, 6, 0)},
            {"value": True, "t": datetime.datetime(2018, 1, 1, 12, 10, 0)},
            {"value": False, "t": datetime.datetime(2018, 1, 1, 12, 15, 0)},
        ]
    ).set_index("t")

    session.add(TemporalBools(tdata=df,))
    session.commit()

    sql = session.query(TemporalBools).filter(TemporalBools.id == 1)
    assert sql.count() == 1

    results = sql.all()
    for result in results:
        assert result.id == 1
        assert result.tdata.size == 3
        assert result.tdata.iloc[0].value == False
        assert result.tdata.iloc[0].name == datetime.datetime(2018, 1, 1, 12, 0, tzinfo=datetime.timezone.utc)
        assert result.tdata.iloc[1].value == True
        assert result.tdata.iloc[1].name == datetime.datetime(2018, 1, 1, 12, 6, tzinfo=datetime.timezone.utc)
        assert result.tdata.iloc[2].value == False
        assert result.tdata.iloc[2].name == datetime.datetime(2018, 1, 1, 12, 15, tzinfo=datetime.timezone.utc)


def test_float_values_are_invalid(session):
    df = pd.DataFrame(
        [
            {"value": 0, "t": datetime.datetime(2018, 1, 1, 12, 0, 0)},
            {"value": 8.1, "t": datetime.datetime(2018, 1, 1, 12, 6, 0)},
        ]
    ).set_index("t")

    with pytest.raises(StatementError):
        session.add(TemporalBools(tdata=df,))
        session.commit()


def test_str_values_are_invalid(session):
    df = pd.DataFrame(
        [
            {"value": "True", "t": datetime.datetime(2018, 1, 1, 12, 0, 0)},
            {"value": "False", "t": datetime.datetime(2018, 1, 1, 12, 6, 0),},
        ]
    ).set_index("t")

    with pytest.raises(StatementError):
        session.add(TemporalBools(tdata=df,))
        session.commit()
