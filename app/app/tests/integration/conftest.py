import os

import pytest
from sqlalchemy.engine import Connection  # type: ignore
from sqlalchemy import orm  # type: ignore

from app.db.session import engine
from app.tests.utils import TestType

Session = orm.sessionmaker()


@pytest.fixture(scope="module")
def connection() -> Connection:
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture(scope="function")
def db(connection) -> orm.Session:
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session  # type: ignore
    session.close()
    transaction.rollback()


@pytest.fixture()
def get_resource(get_resource_for_test_type):
    return get_resource_for_test_type(
        test_type=TestType(os.path.dirname(__file__).split("/")[-1])
    )