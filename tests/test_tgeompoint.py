import datetime
import math

import numpy as np
import pandas as pd
import pytest
import pytz
from shapely.geometry import Point
from shapely.wkt import loads
from sqlalchemy import alias, func
from sqlalchemy.exc import StatementError

from mobilitydb_sqlalchemy.utils import epoch
from .models import Trips, TripsWithMovingPandas


def test_simple_insert(session):
    df = pd.DataFrame(
        [
            {"geometry": Point(0, 0), "t": datetime.datetime(2012, 1, 1, 8, 0, 0),},
            {"geometry": Point(2, 0), "t": datetime.datetime(2012, 1, 1, 8, 10, 0),},
            {"geometry": Point(2, -1.9), "t": datetime.datetime(2012, 1, 1, 8, 15, 0),},
        ]
    ).set_index("t")

    session.add(Trips(car_id=1, trip_id=1, trip=df,))
    session.commit()

    sql = session.query(Trips).filter(Trips.trip_id == 1)
    assert sql.count() == 1

    results = sql.all()
    for result in results:
        assert result.car_id == 1
        assert result.trip_id == 1
        assert result.trip.size == 3
        assert result.trip.iloc[0].geometry == Point(0, 0)
        assert result.trip.iloc[1].geometry == Point(2, 0)
        assert result.trip.iloc[2].geometry == Point(2, -1.9)


def test_simple_insert_with_movingpandas(session):
    import movingpandas as mpd
    from geopandas import GeoDataFrame
    from fiona.crs import from_epsg
    CRS_METRIC = from_epsg(31256)

    df = pd.DataFrame(
        [
            {"geometry": Point(0, 0), "t": datetime.datetime(2012, 1, 1, 8, 0, 0),},
            {"geometry": Point(2, 0), "t": datetime.datetime(2012, 1, 1, 8, 10, 0),},
            {
                "geometry": Point(2, -1.98),
                "t": datetime.datetime(2012, 1, 1, 8, 15, 0),
            },
        ]
    ).set_index("t")
    geo_df = GeoDataFrame(df, crs=CRS_METRIC)
    traj = mpd.Trajectory(geo_df, 1)
    session.add(TripsWithMovingPandas(car_id=1, trip_id=1, trip=traj,))
    session.commit()

    sql = session.query(TripsWithMovingPandas).filter(
        TripsWithMovingPandas.trip_id == 1
    )
    assert sql.count() == 1

    results = sql.all()
    for result in results:
        assert result.car_id == 1
        assert result.trip_id == 1
        assert result.trip.df.size == 3
        assert result.trip.df.iloc[0].geometry == Point(0, 0)
        assert result.trip.df.iloc[1].geometry == Point(2, 0)
        assert result.trip.df.iloc[2].geometry == Point(2, -1.98)


def test_wkt_values_are_valid(session):
    df = pd.DataFrame(
        [
            {
                "geometry": "Point(-3.1 4.7770)",
                "t": datetime.datetime(2012, 1, 1, 12, 0, 0),
            },
        ]
    ).set_index("t")

    with pytest.raises(StatementError):
        session.add(Trips(car_id=1, trip_id=1, trip=df,))
        session.commit()


def test_str_values_are_invalid(session):
    df = pd.DataFrame(
        [
            {"geometry": 0, "t": datetime.datetime(2012, 1, 1, 12, 0, 0)},
            {"geometry": "8", "t": datetime.datetime(2012, 1, 1, 12, 6, 0)},
        ]
    ).set_index("t")

    with pytest.raises(StatementError):
        session.add(Trips(car_id=1, trip_id=1, trip=df,))
        session.commit()


def test_float_values_are_invalid(session):
    df = pd.DataFrame(
        [{"geometry": 8.1, "t": datetime.datetime(2012, 1, 1, 12, 6, 0)},]
    ).set_index("t")

    with pytest.raises(StatementError):
        session.add(Trips(car_id=1, trip_id=1, trip=df,))
        session.commit()


def test_mobility_functions(session):
    df1 = pd.DataFrame(
        [
            {"geometry": Point(0, 0), "t": datetime.datetime(2012, 1, 1, 8, 0, 0),},
            {"geometry": Point(2, 0), "t": datetime.datetime(2012, 1, 1, 8, 10, 0),},
            {"geometry": Point(2, 1), "t": datetime.datetime(2012, 1, 1, 8, 15, 0),},
        ]
    ).set_index("t")

    session.add(Trips(car_id=10, trip_id=1, trip=df1,))

    session.commit()

    df2 = pd.DataFrame(
        [
            {"geometry": Point(0, 0), "t": datetime.datetime(2012, 1, 1, 8, 5, 0),},
            {"geometry": Point(1, 1), "t": datetime.datetime(2012, 1, 1, 8, 10, 0),},
            {"geometry": Point(3, 3), "t": datetime.datetime(2012, 1, 1, 8, 20, 0),},
        ]
    ).set_index("t")

    session.add(Trips(car_id=20, trip_id=1, trip=df2,))

    session.commit()

    # Value at a given timestamp
    trips = session.query(
        Trips.car_id,
        func.asText(
            func.valueAtTimestamp(Trips.trip, datetime.datetime(2012, 1, 1, 8, 10, 0))
        ),
    ).all()

    assert len(trips) == 2
    assert trips[0][0] == 10
    assert loads(trips[0][1]) == Point(2, 0)
    assert trips[1][0] == 20
    assert loads(trips[1][1]) == Point(1, 1)

    # Restriction to a given value
    trips = session.query(
        Trips.car_id, func.asText(func.atValue(Trips.trip, Point(2, 0).wkt)),
    ).all()

    assert len(trips) == 2
    assert trips[0][0] == 10
    assert trips[0][1] == r"{[POINT(2 0)@2012-01-01 08:10:00+00]}"
    assert trips[1][0] == 20
    assert trips[1][1] is None

    # Restriction to a period
    trips = session.query(
        Trips.car_id,
        func.asText(
            func.atPeriod(Trips.trip, "[2012-01-01 08:05:00,2012-01-01 08:10:00]")
        ),
    ).all()

    assert len(trips) == 2
    assert trips[0][0] == 10
    assert (
        trips[0][1]
        == r"[POINT(1 0)@2012-01-01 08:05:00+00, POINT(2 0)@2012-01-01 08:10:00+00]"
    )
    assert trips[1][0] == 20
    assert (
        trips[1][1]
        == r"[POINT(0 0)@2012-01-01 08:05:00+00, POINT(1 1)@2012-01-01 08:10:00+00]"
    )

    # Temporal distance
    T1 = alias(Trips)
    T2 = alias(Trips)
    trips = (
        session.query(T1.c.car_id, T2.c.car_id, T1.c.trip.distance(T2.c.trip),)
        .filter(T1.c.car_id < T2.c.car_id,)
        .all()
    )

    assert len(trips) == 1
    assert trips[0][0] == 10
    assert trips[0][1] == 20
    trips[0][2].index = trips[0][2].index.astype(np.int64)
    # Car #10 would be at (1, 0) and car #20 at (0, 0)
    assert trips[0][2].iloc[0].value == 1
    assert trips[0][2].iloc[0].name == epoch(2012, 1, 1, 8, 5)
    # Car #10 would be at (2, 0) and car #20 at (1, 1)
    assert trips[0][2].iloc[1].value == pytest.approx(math.sqrt(2))
    assert trips[0][2].iloc[1].name == epoch(2012, 1, 1, 8, 10)
    # Car #10 would be at (2, 1) and car #20 at (2, 2)
    assert trips[0][2].iloc[2].value == 1
    assert trips[0][2].iloc[2].name == epoch(2012, 1, 1, 8, 15)
