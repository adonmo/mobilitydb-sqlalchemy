.. image:: https://github.com/adonmo/mobilitydb-sqlalchemy/workflows/Tests/badge.svg
   :target: https://github.com/adonmo/mobilitydb-sqlalchemy/workflows/Tests/badge.svg
   :alt: Test Status

.. image:: https://readthedocs.org/projects/mobilitydb-sqlalchemy/badge/?version=latest
   :target: https://mobilitydb-sqlalchemy.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

MobilityDB SQLAlchemy
================================================================================================================================================================================================================================================================================================================================================================================================================================

This package provides extensions to `SQLAlchemy <http://sqlalchemy.org/>`_ for interacting with `MobilityDB <https://github.com/ULB-CoDE-WIT/MobilityDB>`_. The data retrieved from the database is directly mapped to time index pandas DataFrame objects. Thanks to the amazing work by `MobilityDB <https://github.com/ULB-CoDE-WIT/MobilityDB>`_ and `movingpandas <https://github.com/anitagraser/movingpandas>`_ teams, because of which this project exists.

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

For more details, read our `documentation <https://mobilitydb-sqlalchemy.readthedocs.io/en/latest/>`_

Contributing
============

Issues and pull requests are welcome.

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

movingpandas is an optional dependency - but to run tests you would need it. So if this is your first time rnning tests, install it by running:

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

Now, you can actually run the tests using:

.. code-block:: sh

   poetry run pytest
