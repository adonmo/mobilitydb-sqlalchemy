import datetime
import pytest
from pymeos.box import STBox
from sqlalchemy.exc import StatementError

from .models import STBoxes


def test_simple_insert(session):
    stbox = STBox(
        11,
        12,
        13,
        datetime.datetime(2018, 1, 1, tzinfo=datetime.timezone.utc),
        21,
        22,
        23,
        datetime.datetime(2018, 1, 2, tzinfo=datetime.timezone.utc),
    )

    session.add(STBoxes(stbox=stbox))
    session.commit()

    sql = session.query(STBoxes).filter(STBoxes.id == 1)
    assert sql.count() == 1

    results = sql.all()
    for result in results:
        assert result.id == 1
        assert result.stbox.xmin == 11
        assert result.stbox.ymin == 12
        assert result.stbox.zmin == 13
        assert result.stbox.tmin == datetime.datetime(
            2018, 1, 1, tzinfo=datetime.timezone.utc
        )
        assert result.stbox.xmax == 21
        assert result.stbox.ymax == 22
        assert result.stbox.zmax == 23
        assert result.stbox.tmax == datetime.datetime(
            2018, 1, 2, tzinfo=datetime.timezone.utc
        )


def test_str_values_are_invalid(session):
    stbox = "STBOX ZT((11, 12, 13, 2011-01-01T00:00:00+0000), (21, 22, 23, 2011-01-02T00:00:00+0000))"

    with pytest.raises(StatementError):
        session.add(STBoxes(stbox=stbox))
        session.commit()
