import datetime
import pandas as pd
import pytest
from pymeos.time import Period
from sqlalchemy.exc import StatementError

from .models import Periods


def test_simple_insert(session):
    period = Period(
        datetime.datetime(2018, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2018, 1, 2, tzinfo=datetime.timezone.utc),
    )

    session.add(Periods(period=period))
    session.commit()

    sql = session.query(Periods).filter(Periods.id == 1)
    assert sql.count() == 1

    results = sql.all()
    for result in results:
        assert result.id == 1
        assert result.period.lower == datetime.datetime(
            2018, 1, 1, tzinfo=datetime.timezone.utc
        )
        assert result.period.upper == datetime.datetime(
            2018, 1, 2, tzinfo=datetime.timezone.utc
        )


def test_str_values_are_invalid(session):
    period = "PERIOD (20 30)"

    with pytest.raises(StatementError):
        session.add(Periods(period=period))
        session.commit()
