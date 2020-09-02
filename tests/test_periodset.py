import datetime
import pandas as pd
import pytest
from pymeos.time import Period, PeriodSet
from sqlalchemy.exc import StatementError

from .models import PeriodSets


def test_simple_insert(session):
    period_1 = Period(
        datetime.datetime(2018, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2018, 1, 2, tzinfo=datetime.timezone.utc),
    )
    period_2 = Period(
        datetime.datetime(2018, 1, 10, tzinfo=datetime.timezone.utc),
        datetime.datetime(2018, 1, 11, tzinfo=datetime.timezone.utc),
    )
    periodset = PeriodSet({period_1, period_2})

    session.add(PeriodSets(periodset=periodset))
    session.commit()

    sql = session.query(PeriodSets).filter(PeriodSets.id == 1)
    assert sql.count() == 1

    results = sql.all()
    for result in results:
        assert result.id == 1
        assert result.periodset == periodset
        assert result.periodset.periods == {period_1, period_2}
        assert result.periodset.startPeriod == period_1
        assert result.periodset.endPeriod == period_2


def test_str_values_are_invalid(session):
    periodset = "{PERIOD (20 30), PERIOD (50 60)}"

    with pytest.raises(StatementError):
        session.add(PeriodSets(periodset=periodset))
        session.commit()
