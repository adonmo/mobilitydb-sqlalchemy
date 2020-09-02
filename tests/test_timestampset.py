import datetime
import pytest
from pymeos.time import TimestampSet
from sqlalchemy.exc import StatementError

from .models import TimestampSets


def test_simple_insert(session):
    dt_1 = datetime.datetime(2018, 1, 1, tzinfo=datetime.timezone.utc)
    dt_2 = datetime.datetime(2018, 1, 2, tzinfo=datetime.timezone.utc)
    timestampset = TimestampSet({dt_1, dt_2})

    session.add(TimestampSets(timestampset=timestampset))
    session.commit()

    sql = session.query(TimestampSets).filter(TimestampSets.id == 1)
    assert sql.count() == 1

    results = sql.all()
    for result in results:
        assert result.id == 1
        assert result.timestampset == timestampset
        assert result.timestampset.timestamps == {dt_1, dt_2}
        assert result.timestampset.startTimestamp == dt_1
        assert result.timestampset.endTimestamp == dt_2


def test_str_values_are_invalid(session):
    timestampset = "{2020-01-01, 2020-01-02}"

    with pytest.raises(StatementError):
        session.add(TimestampSets(timestampset=timestampset))
        session.commit()
