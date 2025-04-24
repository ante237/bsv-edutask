import pytest
import pymongo
import os
import json

from unittest.mock import MagicMock, patch
from src.util.dao import DAO
from dotenv import dotenv_values
from src.util.validators import getValidator


class MockedDAO(DAO):
    def __init__ (self, collection_name: str):
        validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["requiredString"],
                "properties": {
                    "requiredString":{
                        "bsonType": "string",
                        "description": "required string for test",
                        "uniqueItems": True
                    },
                    "uniqueString":{
                        "bsonType": "string",
                        "description": "unique string for test",
                        "uniqueItems": True
                    },
                    "nonRequiredString":{
                        "bsonType": "string",
                        "description": "Non-required string for test"
                    },
                    "testBool":{
                        "bsonType": "bool",
                        "description": "bool for test"
                    }
                }
            }
        }
        # load the local mongo URL (something like mongodb://localhost:27017)
        LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
        # check out of the environment (which can be overridden by the docker-compose file) also specifies an URL, and use that instead if it exists
        MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)

        # connect to the MongoDB and select the appropriate database
        print(
            f'Connecting to collection test on MongoDB at url {MONGO_URL}')
        client = pymongo.MongoClient("mongodb://root:root@localhost:27017/")
        database = client.test_db

        # create the collection if it does not yet exist
        if "test" not in database.list_collection_names():
            validator = getValidator("test")
            database.create_collection("test", validator=self.validator)

        self.collection = database["test"]

   
@pytest.mark.daocreate
class TestDAO:
    def test_1(self):
        obj = MockedDAO("test")
        # Inserting objects that fulfill the requirements
        result1 = obj.create({"requiredString": "test_required", "uniqueString": "test_unique", "nonRequiredString": "test_nonrequired", "testBool": True})
        result2 = obj.create({"requiredString": "test_required_unique", "uniqueString": "test_unique2", "nonRequiredString": "test_nonrequired", "testBool": True})

        assert result2["_id"] != None
        assert result2["requiredString"] == "test_required_unique"
        assert result2["uniqueString"] == "test_unique2"
        assert result2["nonRequiredString"] == "test_nonrequired"
        assert result2["testBool"] == True
        

    def test_2(self):
        obj = MockedDAO("test")
        result1 = obj.create({"requiredString": "test_required", "nonRequiredString": "test_nonrequired", "testBool": True})
        # Inserting object that only has required fields
        result2 = obj.create({"requiredString": "test_required_unique"})

        assert result2["_id"] != None
        assert result2["requiredString"] == "test_required_unique"

    def test_3(self):
        obj = MockedDAO("test")

        with pytest.raises(pymongo.errors.WriteError):
            # Inserting object with duplicate unique string
            result1 = obj.create({"requiredString": "test_required", "uniqueString": "test_unique", "nonRequiredString": "test_nonrequired", "testBool": True})
            result2 = obj.create({"requiredString": "test_required_unique", "uniqueString": "test_unique", "nonRequiredString": "test_nonrequired", "testBool": True})
            print(result1)
            print(result2)

    def test_4(self):
        obj = MockedDAO("test")

        with pytest.raises(pymongo.errors.WriteError):
            # Inserting object with duplicate requiredString
            result1 = obj.create({"requiredString": "test_required", "uniqueString": "test_unique", "nonRequiredString": "test_nonrequired", "testBool": True})
            result2 = obj.create({"requiredString": "test_required_unique","uniqueString": "test_unique2", "nonRequiredString": True, "testBool": "test_nonrequired"})

    def test_5(self):
        obj = MockedDAO("test")

        with pytest.raises(pymongo.errors.WriteError):
            # Inserting object with duplicate requiredString
            result1 = obj.create({"requiredString": "test_required", "uniqueString": "test_unique", "nonRequiredString": "test_nonrequired", "testBool": True})
            result2 = obj.create({"requiredString": "test_required_unique","uniqueString": "test_unique", "nonRequiredString": True, "testBool": "test_nonrequired"})

    def test_6(self):
        obj = MockedDAO("test")

        with pytest.raises(pymongo.errors.WriteError):
            # Inserting object with duplicate requiredString
            result1 = obj.create({"requiredString": "test_required", "uniqueString": "test_unique", "nonRequiredString": "test_nonrequired", "testBool": True})
            result2 = obj.create({"uniqueString": "test_unique2", "nonRequiredString": "test_nonrequired", "testBool": True})

    def test_7(self):
        obj = MockedDAO("test")

        with pytest.raises(pymongo.errors.WriteError):
            # Inserting object with duplicate requiredString
            result1 = obj.create({"requiredString": "test_required", "uniqueString": "test_unique", "nonRequiredString": "test_nonrequired", "testBool": True})
            result2 = obj.create({"uniqueString": "test_unique", "nonRequiredString": "test_nonrequired", "testBool": True})

    def test_8(self):
        obj = MockedDAO("test")

        with pytest.raises(pymongo.errors.WriteError):
            # Inserting object with duplicate requiredString
            result1 = obj.create({"requiredString": "test_required", "uniqueString": "test_unique", "nonRequiredString": "test_nonrequired", "testBool": True})
            result2 = obj.create({"uniqueString": "test_unique2", "nonRequiredString": True, "testBool": "test_nonrequired"})

    def test_9(self):
        obj = MockedDAO("test")

        with pytest.raises(pymongo.errors.WriteError):
            # Inserting object with duplicate requiredString
            result1 = obj.create({"requiredString": "test_required", "uniqueString": "test_unique", "nonRequiredString": "test_nonrequired", "testBool": True})
            result2 = obj.create({"uniqueString": "test_unique", "nonRequiredString": True, "testBool": "test_nonrequired"})
