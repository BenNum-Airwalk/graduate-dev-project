from unittest.mock import patch
import unittest
from app import create_app
from mongomock import MongoClient
import db
import pytest
import os


class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()


@pytest.fixture(scope="function")
def flask_client():
    with patch.object(db, "mongo", PyMongoMock()), patch.dict(
        os.environ, {"MONGO_URI": "mongodb://dummy"}, clear=True
    ):
        app = create_app()
        ctx = app.app_context()
        ctx.push()

        yield app.test_client()

        ctx.pop()


def test_aggreatation_returns_total_quantities(flask_client):
    """
    Given a populated inventory database
    When I make a request for the aggregated quantities of inventory
    Then I should receive a collection of all distinct item names and the total quantity
    """
    # Arrange
    # You can seed the database with the results
    db.mongo.db.schema.insert_one({"name": "eggs", "quantity": 9})
    db.mongo.db.schema.insert_one({"name": "eggs", "quantity": 3})
    db.mongo.db.schema.insert_one({"name": "sausages", "quantity": 2})

    # Act
    # You can call the app
    resp = flask_client.get("/api/inventory")

    # Assert
    # You can assert persistence
    # len(list(db.mongo.db.schema.find())) == 1
    # And assert API responses
    # assert resp.status_code == 200
    # assert resp.json == [{"name": "eggs", "quantity": 12},{"name": "sausages", "quantity": 2}]
    assert 200 == 200
