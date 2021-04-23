**********
Quickstart
**********

Temporal data
-------------

mobilitydb-sqlalchemy lets you use pandas DataFrame (which are great for timeseries data) while you are in the Python world, and translates it back and for to temporal types defined in mobilitydb.

A point to note here is that we assume that the DataFrame's columns are named "value" (except in case of TGeomPoint where it is "geometry") and "t" for the data and the timestamp respectively.

Here we show how we can store numeric data which changes over time (i.e. tfloat), using the :class:`mobilitydb_sqlalchemy.types.TFloat.TFloat` class.

Running the following code will create a new table with a tfloat column, and insert one row of hardcoded data into it.


Write data to MobilityDB
........................

.. code-block:: python
    :emphasize-lines: 4, 19, 32, 33, 34

    import datetime
    import pandas as pd

    from mobilitydb_sqlalchemy import TFloat
    from sqlalchemy import Column, Integer, create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    # Setup the engine and session, make sure you set the right url to connect to your mobilitydb instance
    engine = create_engine("postgresql://docker:docker@localhost:25432/mobilitydb", echo=True)
    session = sessionmaker(bind=engine)()

    # Setup and create the tables (only one in our case here)
    Base = declarative_base()

    class TemporalFloats(Base):
        __tablename__ = "tfloat_test_001"
        id = Column(Integer, primary_key=True)
        tdata = Column(TFloat(True, False))

    Base.metadata.create_all(engine)

    # Prepare and insert the data
    df = pd.DataFrame(
        [
            {"value": 0, "t": datetime.datetime(2018, 1, 1, 12, 0, 0)},
            {"value": 8.2, "t": datetime.datetime(2018, 1, 1, 12, 6, 0)},
            {"value": 6.6, "t": datetime.datetime(2018, 1, 1, 12, 10, 0)},
            {"value": 9.1, "t": datetime.datetime(2018, 1, 1, 12, 15, 0)},
        ]
    ).set_index("t")
    row = TemporalFloats(tdata=df,)
    session.add(row)
    session.commit()


Geometric data
--------------

While creating the DataFrame, make sure the column is named "geometry" and not "value". This is to maintain compatibility with movingpandas. We can use Point objects from shapely for preparing the geometry data.


Writing
.......

.. code-block:: python
    :emphasize-lines: 4, 5, 19, 32, 33, 34

    import datetime
    import pandas as pd

    from mobilitydb_sqlalchemy import TGeomPoint
    from shapely.geometry import Point
    from sqlalchemy import Column, Integer, create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    engine = create_engine("postgresql://docker:docker@db:25432/mobilitydb", echo=True)
    session = sessionmaker(bind=engine)()

    Base = declarative_base()

    class Trips(Base):
        __tablename__ = "trips_test_001"
        car_id = Column(Integer, primary_key=True)
        trip_id = Column(Integer, primary_key=True)
        trip = Column(TGeomPoint)

    Base.metadata.create_all(engine)

    # Prepare and insert the data
    df = pd.DataFrame(
        [
            {"geometry": Point(0, 0), "t": datetime.datetime(2012, 1, 1, 8, 0, 0),},
            {"geometry": Point(2, 0), "t": datetime.datetime(2012, 1, 1, 8, 10, 0),},
            {"geometry": Point(2, -1.9), "t": datetime.datetime(2012, 1, 1, 8, 15, 0),},
        ]
    ).set_index("t")

    trip = Trips(car_id=1, trip_id=1, trip=df,)
    session.add(trip)
    session.commit()


Querying
........

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

Inserting TGeomPoint data, using movingpandas
---------------------------------------------

movingpandas is an optional dependency, but if installed, you can insert TGeomPoint data with Trajectory objects directly. Just be sure to enable the flag use_movingpandas on the column beforehand.

.. code-block:: python
    :emphasize-lines: 6, 7, 24, 36, 38, 42, 43, 44

    import datetime
    import pandas as pd
    from geopandas import GeoDataFrame
    import movingpandas as mpd

    from mobilitydb_sqlalchemy import TGeomPoint
    from shapely.geometry import Point
    from sqlalchemy import Column, Integer, create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    from fiona.crs import from_epsg
    CRS_METRIC = from_epsg(31256)

    engine = create_engine("postgresql://docker:docker@db:25432/mobilitydb", echo=True)
    session = sessionmaker(bind=engine)()

    Base = declarative_base()

    class Trips(Base):
        __tablename__ = "trips_test_002"
        car_id = Column(Integer, primary_key=True)
        trip_id = Column(Integer, primary_key=True)
        trip = Column(TGeomPoint(use_movingpandas=True))

    Base.metadata.create_all(engine)

    # Prepare and insert the data
    df = pd.DataFrame(
        [
            {"geometry": Point(0, 0), "t": datetime.datetime(2012, 1, 1, 8, 0, 0),},
            {"geometry": Point(2, 0), "t": datetime.datetime(2012, 1, 1, 8, 10, 0),},
            {"geometry": Point(2, -1.9), "t": datetime.datetime(2012, 1, 1, 8, 15, 0),},
        ]
    ).set_index("t")
    geo_df = GeoDataFrame(df, crs=CRS_METRIC)

    traj = mpd.Trajectory(geo_df, 1)
    # Note: In case you are depending on movingpandas 0.1 or lower,
    # you might need to do mpd.Trajectory(1, geo_df) instead

    trip = Trips(car_id=1, trip_id=1, trip=traj,)
    session.add(trip)
    session.commit()


Querying data from MobilityDB
-----------------------------

SQLAlchemy's `func` is pretty generic and flexible, allowing us to use MobilityDB's functions without needing any new constructs.

Let's take few example queries from MobilityDB's documentation, and explain how we can achieve the same using this package.

.. code-block:: python

    from sqlalchemy import func
    from shapely.wkt import loads


Value at a given timestamp
..........................

.. code-block:: sql

    SELECT CarId, ST_AsText(valueAtTimestamp(Trip, timestamptz '2012-01-01 08:10:00')) FROM Trips;
    -- 10;"POINT(2 0)"
    -- 20;"POINT(1 1)"


.. code-block:: python

    session.query(
        Trips.car_id,
        func.asText(
            func.valueAtTimestamp(Trips.trip, datetime.datetime(2012, 1, 1, 8, 10, 0))
        ),
    ).all()

Restriction to a given value
............................

.. code-block:: sql

    SELECT CarId, asText(atValue(Trip, 'Point(2 0)'))
    FROM Trips;
    -- 10;"{"[POINT(2 0)@2012-01-01 08:10:00+00]"}"
    -- 20; NULL

.. code-block:: python

    session.query(
        Trips.car_id,
        func.asText(func.atValue(Trips.trip, Point(2, 0).wkt)),
    ).all()


Restriction to a period
.......................

.. code-block:: sql

    SELECT CarId, asText(atPeriod(Trip, '[2012-01-01 08:05:00,2012-01-01 08:10:00]'))
    FROM Trips;
    -- 10;"{[POINT(1 0)@2012-01-01 08:05:00+00, POINT(2 0)@2012-01-01 08:10:00+00]}"
    -- 20;"{[POINT(0 0)@2012-01-01 08:05:00+00, POINT(1 1)@2012-01-01 08:10:00+00]}"

.. code-block:: python

    session.query(
        Trips.car_id,
        func.asText(
            func.atPeriod(Trips.trip, "[2012-01-01 08:05:00,2012-01-01 08:10:00]")
        ),
    ).all()


Temporal distance
.................

..
    This part needs further Explanation. Please elaborate where does T1, T2 come from?

.. code-block:: sql

    -- Temporal distance
    SELECT T1.CarId, T2.CarId, T1.Trip <-> T2.Trip
    FROM Trips T1, Trips T2
    WHERE T1.CarId < T2.CarId;
    -- 10;20;"{[1@2012-01-01 08:05:00+00, 1.4142135623731@2012-01-01 08:10:00+00, 1@2012-01-01 08:15:00+00)}"

.. code-block:: python

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
TGeomPoint objects can also be optionally mapped to movingpandas Trajectory objects.

For this the optional dependency "movingpandas" needs to be installed.

.. code-block:: sh

    poetry install -E movingpandas


After this, movingpandas can be enabled with a flag on the TGeomPoint column

.. code-block:: python
    :emphasize-lines: 3

    class Trips(Base):
        trip_id = Column(Integer, primary_key=True)
        trip = Column(TGeomPoint(use_movingpandas=True))
