import datetime
import pytest
from pymeos.range import RangeInt
from sqlalchemy.exc import StatementError

from .models import RangeInts


def test_simple_insert(session):
    rangeint = RangeInt(10, 20)

    session.add(RangeInts(rangeint=rangeint))
    session.commit()

    sql = session.query(RangeInts).filter(RangeInts.id == 1)
    assert sql.count() == 1

    results = sql.all()
    for result in results:
        assert result.id == 1
        assert str(result.rangeint) == "[10, 20)"
        assert result.rangeint.lower == 10
        assert result.rangeint.upper == 20
        assert result.rangeint.lower_inc == True
        assert result.rangeint.upper_inc == False


def test_str_values_are_invalid(session):
    rangeint = "[10, 20)"

    with pytest.raises(StatementError):
        session.add(RangeInts(rangeint=rangeint))
        session.commit()
