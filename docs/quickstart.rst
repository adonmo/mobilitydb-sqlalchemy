Quickstart
----------

.. code-block:: python
    :emphasize-lines: 1, 11, 19
    :caption: Example usage of the **TGeomPoint** class as a column in a table defined using SQLAlchemy's declarative API

    from mobilitydb_sqlalchemy import TGeomPoint

    from sqlalchemy import Column, Integer
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()

    class Trips(Base):
        __tablename__ = "test_table_trips_01"
        car_id = Column(Integer, primary_key=True)
        trip_id = Column(Integer, primary_key=True)
        trip = Column(TGeomPoint)

    trips = session.query(Trips).all()

    # Querying using MobilityDB functions, for example - valueAtTimestamp
    session.query(
        Trips.car_id,
        func.asText(
            func.valueAtTimestamp(Trips.trip, datetime.datetime(2012, 1, 1, 8, 10, 0))
        ),
    ).all()


Using MobilityDB functions
--------------------------

SQLAlchemy's `func` is pretty generic and flexible, allowing us to use MobilityDB's functions without needing any new constructs.

Let's take few example queries from MobilityDB's documentation, and explain how we can achieve the same using this package.

.. code-block:: sql

    -- Value at a given timestamp
    SELECT CarId, ST_AsText(valueAtTimestamp(Trip, timestamptz '2012-01-01 08:10:00')) FROM Trips;
    -- 10;"POINT(2 0)"
    -- 20;"POINT(1 1)"

    -- Restriction to a given value
    SELECT CarId, asText(atValue(Trip, 'Point(2 0)'))
    FROM Trips;
    -- 10;"{"[POINT(2 0)@2012-01-01 08:10:00+00]"}"
    -- 20; NULL

    -- Restriction to a period
    SELECT CarId, asText(atPeriod(Trip, '[2012-01-01 08:05:00,2012-01-01 08:10:00]'))
    FROM Trips;
    -- 10;"{[POINT(1 0)@2012-01-01 08:05:00+00, POINT(2 0)@2012-01-01 08:10:00+00]}"
    -- 20;"{[POINT(0 0)@2012-01-01 08:05:00+00, POINT(1 1)@2012-01-01 08:10:00+00]}"

    -- Temporal distance
    SELECT T1.CarId, T2.CarId, T1.Trip <-> T2.Trip
    FROM Trips T1, Trips T2
    WHERE T1.CarId < T2.CarId;
    -- 10;20;"{[1@2012-01-01 08:05:00+00, 1.4142135623731@2012-01-01 08:10:00+00, 1@2012-01-01 08:15:00+00)}"

.. code-block:: python

    from sqlalchemy import func
    from shapely.wkt import loads

    # Value at a given timestamp
    session.query(
        Trips.car_id,
        func.asText(
            func.valueAtTimestamp(Trips.trip, datetime.datetime(2012, 1, 1, 8, 10, 0))
        ),
    ).all()

    # Restriction to a given value
    session.query(
        Trip.car_id,
        func.asText(func.atValue(Trips.trip, Point(2, 0).wkt)),
    ).all()

    # Restriction to a period
    session.query(
        Trips.car_id,
        func.asText(
            func.atPeriod(Trips.trip, "[2012-01-01 08:05:00,2012-01-01 08:10:00]")
        ),
    ).all()

    # Temporal distance
    session.query(
        T1.c.car_id,
        T2.c.car_id,
        T1.c.trip.distance(T2.c.trip),
    ) \
    .filter(T1.c.car_id < T2.c.car_id,)
    .all()


Using MobilityDB operators
--------------------------

.. code-block:: python
    :emphasize-lines: 4
    :caption: Example usage of the distance operator ('<->')

    session.query(
        T1.c.car_id,
        T2.c.car_id,
        T1.c.trip.distance(T2.c.trip),
    ) \
    .filter(T1.c.car_id < T2.c.car_id,)
    .all()

For exhaustive listing of operators, see :doc:`operators page </operators>`.


Using MobilityDB ranges
-----------------------
MobilityDB also allows you to store the temporal data in either open or closed intervals on either site. While this is supported by the package at the column level, because we use pandas DataFrame to hold the values once we load them into python runtime, this data is lost, and hence not of much use. In future, this can be avoided with a better suiting data structure to hold this data instead of relying on pandas.

However, to define a column which stores temporal data as a left closed, right open interval, ie. '[)', it can be done as shown below:

.. code-block:: python
    :emphasize-lines: 3

    class Trips(Base):
        trip_id = Column(Integer, primary_key=True)
        trip = Column(TGeomPoint(True, False))


Making use of movingpandas Trajectory data structure
----------------------------------------------------
TGeomPoint objects can also be optioanlly mapped to movingpandas Trajectory objects.

For this the optional dependency "movingpandas" needs to be installed.

.. code-block:: sh

    # Currently installing the optional dependency of movingpandas
    # using `poetry install -E movingpandas` doesn't work

    # To get movingpandas use pip instead of poetry, run the following (in exact order):
    poetry shell
    pip install cython
    pip install git+https://github.com/SciTools/cartopy.git --no-binary cartopy
    pip install movingpandas
    pip install rasterio --upgrade

    # This is because of movingpandas depencenies rasterio, cython and cartopy:
    # (1) rasterio, cython result in unresolved dependencies
    # (2) cartopy is not PEP 518 compliant
    # Refer: https://github.com/SciTools/cartopy/issues/1112


After this, movingpandas can be enabled with a flag on the TGeomPoint column

.. code-block:: python
    :emphasize-lines: 3

    class Trips(Base):
        trip_id = Column(Integer, primary_key=True)
        trip = Column(TGeomPoint(use_movingpandas=True))
