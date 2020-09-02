import datetime
import pytest
from pymeos.box import TBox
from sqlalchemy.exc import StatementError

from .models import TBoxes


def test_simple_insert(session):
    tbox = TBox(
        datetime.datetime(2018, 1, 1, tzinfo=datetime.timezone.utc),
        datetime.datetime(2018, 1, 2, tzinfo=datetime.timezone.utc),
    )

    session.add(TBoxes(tbox=tbox))
    session.commit()

    sql = session.query(TBoxes).filter(TBoxes.id == 1)
    assert sql.count() == 1

    results = sql.all()
    for result in results:
        assert result.id == 1
        assert result.tbox.tmin == datetime.datetime(
            2018, 1, 1, tzinfo=datetime.timezone.utc
        )
        assert result.tbox.tmax == datetime.datetime(
            2018, 1, 2, tzinfo=datetime.timezone.utc
        )


def test_str_values_are_invalid(session):
    tbox = "TBOX ((20,), (30,))"

    with pytest.raises(StatementError):
        session.add(TBoxes(tbox=tbox))
        session.commit()
