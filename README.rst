.. image:: https://github.com/adonmo/mobilitydb-sqlalchemy/workflows/Tests/badge.svg
   :target: https://github.com/adonmo/mobilitydb-sqlalchemy/actions
   :alt: Test Status

.. image:: https://readthedocs.org/projects/mobilitydb-sqlalchemy/badge/?version=latest
   :target: https://mobilitydb-sqlalchemy.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://pepy.tech/badge/mobilitydb-sqlalchemy
   :target: https://pepy.tech/project/mobilitydb-sqlalchemy
   :alt: PyPI downloads

.. image:: https://img.shields.io/github/license/adonmo/mobilitydb-sqlalchemy.svg
   :target: https://github.com/adonmo/mobilitydb-sqlalchemy/blob/master/LICENSE.txt
   :alt: MIT License

MobilityDB SQLAlchemy
=====================

This package provides extensions to `SQLAlchemy <http://sqlalchemy.org/>`_ for interacting with `MobilityDB <https://github.com/ULB-CoDE-WIT/MobilityDB>`_. The data retrieved from the database is directly mapped to time-indexed pandas DataFrame objects. TGeomPoint and TGeogPoint objects can be optionally mapped to movingpandas' Trajectory data structure.

Thanks to the amazing work by `MobilityDB <https://github.com/ULB-CoDE-WIT/MobilityDB>`_ and `movingpandas <https://github.com/anitagraser/movingpandas>`_ teams, because of which this project exists.

This project is built using `PyMEOS <https://github.com/adonmo/meos>`_

A demo webapp built using this library is now available online:

**Live Demo**: https://mobilitydb-sqlalchemy-demo.adonmo.com

**Source Code**: https://github.com/adonmo/mobilitydb-sqlalchemy-demo

Installation
============

The package is available on `PyPI <https://pypi.org/project/mobilitydb-sqlalchemy>`_\ , for Python >= 3.7

.. code-block:: sh

    pip install mobilitydb-sqlalchemy

Usage
=====

.. code-block:: py

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

There is also a `tutorial <https://anitagraser.com/2020/03/02/movement-data-in-gis-29-power-your-web-apps-with-movement-data-using-mobilitydb-sqlalchemy/>`_ published on Anita Graser's blog.

For more details, read our `documentation <https://mobilitydb-sqlalchemy.readthedocs.io/en/latest/>`_ (specifically, the `quickstart <https://mobilitydb-sqlalchemy.readthedocs.io/en/latest/quickstart.html>`_).

Contributing
============

Issues and pull requests are welcome.

* For proposing new features/improvements or reporting bugs, `create an issue <https://github.com/adonmo/mobilitydb-sqlalchemy/issues/new/choose>`_.
* Check `open issues <https://github.com/adonmo/mobilitydb-sqlalchemy/issues>`_ for viewing existing ideas, verify if it is already proposed/being worked upon.
* When implementing new features make sure to add relavant tests and documentation before sending pull requests.

Setup environment
-----------------

First, make sure you have `poetry installed <https://python-poetry.org/docs/#installation>`_
Then, get the dependencies by running (in the project home directory):

.. code-block:: sh

    poetry install

Also make sure you setup git hooks locally, this will ensure code is formatted using `black <https://github.com/psf/black>`_ before committing any changes to the repository

.. code-block:: sh

    pre-commit install

Running Tests
-------------

Spin up a mobilitydb instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: sh

    docker volume create mobilitydb_data
    docker run --name "mobilitydb" -d -p 25432:5432 -v mobilitydb_data:/var/lib/postgresql codewit/mobilitydb

Run the tests
^^^^^^^^^^^^^

movingpandas is an optional dependency - but to run tests you would need it. So if this is your first time running tests, install it by running:

.. code-block:: sh

    poetry install -E movingpandas

Now, you can actually run the tests using:

.. code-block:: sh

    poetry run pytest
