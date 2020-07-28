import datetime
import math

import numpy as np
import pandas as pd
import pytest
import pytz
import re
from shapely.geometry import Point
from shapely.wkt import loads
from sqlalchemy import alias, func, Text
from sqlalchemy.exc import StatementError
from sqlalchemy.sql.expression import cast

from mobilitydb_sqlalchemy.utils import epoch
from .models import GeogTrips, GeogTripsWithMovingPandas
from .postgis_types import Geometry


def test_simple_insert(session):
    df = pd.DataFrame(
        [
            {"geometry": Point(0, 0), "t": datetime.datetime(2012, 1, 1, 8, 0, 0),},
            {"geometry": Point(2, 0), "t": datetime.datetime(2012, 1, 1, 8, 10, 0),},
            {"geometry": Point(2, -1.9), "t": datetime.datetime(2012, 1, 1, 8, 15, 0),},
        ]
    ).set_index("t")

    session.add(GeogTrips(car_id=1, trip_id=1, trip=df,))
    session.commit()

    sql = session.query(GeogTrips).filter(GeogTrips.trip_id == 1)
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
    session.add(GeogTripsWithMovingPandas(car_id=1, trip_id=1, trip=traj,))
    session.commit()

    sql = session.query(GeogTripsWithMovingPandas).filter(
        GeogTripsWithMovingPandas.trip_id == 1
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
        session.add(GeogTrips(car_id=1, trip_id=1, trip=df,))
        session.commit()


def test_str_values_are_invalid(session):
    df = pd.DataFrame(
        [
            {"geometry": 0, "t": datetime.datetime(2012, 1, 1, 12, 0, 0)},
            {"geometry": "8", "t": datetime.datetime(2012, 1, 1, 12, 6, 0)},
        ]
    ).set_index("t")

    with pytest.raises(StatementError):
        session.add(GeogTrips(car_id=1, trip_id=1, trip=df,))
        session.commit()


def test_float_values_are_invalid(session):
    df = pd.DataFrame(
        [{"geometry": 8.1, "t": datetime.datetime(2012, 1, 1, 12, 6, 0)},]
    ).set_index("t")

    with pytest.raises(StatementError):
        session.add(GeogTrips(car_id=1, trip_id=1, trip=df,))
        session.commit()


def test_mobility_functions(session):
    df1 = pd.DataFrame(
        [
            {"geometry": Point(0, 0), "t": datetime.datetime(2012, 1, 1, 8, 0, 0),},
            {"geometry": Point(2, 0), "t": datetime.datetime(2012, 1, 1, 8, 10, 0),},
            {"geometry": Point(2, 1), "t": datetime.datetime(2012, 1, 1, 8, 15, 0),},
        ]
    ).set_index("t")

    session.add(GeogTrips(car_id=10, trip_id=1, trip=df1,))

    session.commit()

    df2 = pd.DataFrame(
        [
            {"geometry": Point(0, 0), "t": datetime.datetime(2012, 1, 1, 8, 5, 0),},
            {"geometry": Point(1, 1), "t": datetime.datetime(2012, 1, 1, 8, 10, 0),},
            {"geometry": Point(3, 3), "t": datetime.datetime(2012, 1, 1, 8, 20, 0),},
        ]
    ).set_index("t")

    session.add(GeogTrips(car_id=20, trip_id=1, trip=df2,))

    session.commit()

    # Value at a given timestamp
    trips = session.query(
        GeogTrips.car_id,
        func.asText(
            cast(
                func.valueAtTimestamp(
                    GeogTrips.trip, datetime.datetime(2012, 1, 1, 8, 10, 0)
                ),
                Geometry,
            )
        ),
    ).all()

    assert len(trips) == 2
    assert trips[0][0] == 10
    assert loads(trips[0][1]) == Point(2, 0)
    assert trips[1][0] == 20
    assert loads(trips[1][1]) == Point(1, 1)

    # Restriction to a given value
    trips = session.query(
        GeogTrips.car_id, func.asText(func.atValue(GeogTrips.trip, Point(2, 0).wkt)),
    ).all()

    assert len(trips) == 2
    assert trips[0][0] == 10
    assert trips[0][1] == r"{[POINT(2 0)@2012-01-01 08:10:00+00]}"
    assert trips[1][0] == 20
    assert trips[1][1] is None

    # Restriction to a period
    trips = session.query(
        GeogTrips.car_id,
        func.asText(
            func.atPeriod(GeogTrips.trip, "[2012-01-01 08:05:00,2012-01-01 08:10:00]")
        ),
    ).all()

    assert len(trips) == 2
    assert trips[0][0] == 10
    assert pytest.approx(
        float(
            re.search(
                r"\[POINT\((.+?) 0\)@2012-01-01 08:05:00\+00, POINT\(2 0\)@2012-01-01 08:10:00\+00\]",
                str(trips[0][1]),
            ).group(1)
        ),
        1,
    )
    assert trips[1][0] == 20
    assert (
        trips[1][1]
        == r"[POINT(0 0)@2012-01-01 08:05:00+00, POINT(1 1)@2012-01-01 08:10:00+00]"
    )

    # Temporal distance
    T1 = alias(GeogTrips)
    T2 = alias(GeogTrips)
    trips = (
        session.query(T1.c.car_id, T2.c.car_id, T1.c.trip.distance(T2.c.trip),)
        .filter(T1.c.car_id < T2.c.car_id,)
        .all()
    )

    assert len(trips) == 1
    assert trips[0][0] == 10
    assert trips[0][1] == 20
    # Car #10 would be at (1, 0) and car #20 at (0, 0)
    assert pytest.approx(trips[0][2].iloc[0].value, haversine(1, 0, 0, 0))
    assert trips[0][2].iloc[0].name == datetime.datetime(
        2012, 1, 1, 8, 5, tzinfo=datetime.timezone.utc
    )
    # Car #10 would be at (2, 0) and car #20 at (1, 1)
    assert pytest.approx(trips[0][2].iloc[1].value, haversine(2, 0, 1, 1))
    assert trips[0][2].iloc[1].name == datetime.datetime(
        2012, 1, 1, 8, 10, tzinfo=datetime.timezone.utc
    )
    # Car #10 would be at (2, 1) and car #20 at (2, 2)
    assert pytest.approx(trips[0][2].iloc[2].value, haversine(2, 1, 2, 2))
    assert trips[0][2].iloc[2].name == datetime.datetime(
        2012, 1, 1, 8, 15, tzinfo=datetime.timezone.utc
    )


def haversine(lat1, lon1, lat2, lon2, **kwarg):
    """
    This uses the ‘haversine’ formula to calculate the great-circle distance between two points – that is,
    the shortest distance over the earth’s surface – giving an ‘as-the-crow-flies’ distance between the points
    (ignoring any hills they fly over, of course!).
    Haversine
    formula:    a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    c = 2 ⋅ atan2( √a, √(1−a) )
    d = R ⋅ c
    where   φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km);
    note that angles need to be in radians to pass to trig functions!

    Copied from https://stackoverflow.com/a/56769419
    """
    R = 6371.0088
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(a ** 0.5, (1 - a) ** 0.5)
    d = R * c
    return round(d, 4)
