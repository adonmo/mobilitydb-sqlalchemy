import datetime
import pytest
from pymeos.range import RangeFloat
from sqlalchemy.exc import StatementError

from .models import RangeFloats


def test_simple_insert(session):
    rangefloat = RangeFloat(10, 20)

    session.add(RangeFloats(rangefloat=rangefloat))
    session.commit()

    sql = session.query(RangeFloats).filter(RangeFloats.id == 1)
    assert sql.count() == 1

    results = sql.all()
    for result in results:
        assert result.id == 1
        assert str(result.rangefloat) == "[10, 20)"
        assert result.rangefloat.lower == 10
        assert result.rangefloat.upper == 20
        assert result.rangefloat.lower_inc == True
        assert result.rangefloat.upper_inc == False


def test_str_values_are_invalid(session):
    rangefloat = "[10, 20)"

    with pytest.raises(StatementError):
        session.add(RangeFloats(rangefloat=rangefloat))
        session.commit()
