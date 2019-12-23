MobilityDB SQLAlchemy [![Documentation Status](https://readthedocs.org/projects/mobilitydb_sqlalchemy/badge/?version=latest)](https://chaitan94-demo.readthedocs.io/en/latest/?badge=latest)
====
This package provides extensions to [SQLAlchemy](http://sqlalchemy.org/) for interacting with [MobilityDB](https://github.com/ULB-CoDE-WIT/MobilityDB).

# Installation
```sh
pip install mobilitydb-sqlalchemy
```

# Usage

```py
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
```

For more details, read our [documentation](https://mobilitydb-sqlalchemy.readthedocs.io/en/latest/)

# Contributing
Issues and pull requests are welcome.

## Setup environment
First, make sure you have [poetry installed](https://python-poetry.org/docs/#installation)
Then, get the dependencies by running (in the project home directory):
```sh
poetry install
```
Also make sure you setup git hooks locally, this will ensure code is formatted using [black](https://github.com/psf/black) before committing any changes to the repository
```sh
pre-commit install
```

## Running Tests

### Spin up a mobilitydb instance
```sh
docker volume create mobilitydb_data
docker run --name "mobilitydb" -d -p 25432:5432 -v mobilitydb_data:/var/lib/postgresql codewit/mobilitydb
```

### Run the tests
```sh
poetry run pytest
```
