import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


@pytest.fixture(scope="session")
def engine():
    _engine = create_engine(
        "postgresql://docker:docker@localhost:25432/mobilitydb", echo=True
    )
    return _engine


@pytest.yield_fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.yield_fixture(scope="function")
def session(engine, tables):
    connection = engine.connect()
    transaction = connection.begin()

    make_session = sessionmaker()
    make_session.configure(bind=connection)
    _session = make_session()

    yield _session

    transaction.rollback()
    connection.close()
