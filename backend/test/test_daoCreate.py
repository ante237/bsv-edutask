import pytest
import pymongo
import os
import json

from unittest.mock import MagicMock, patch
from src.util.dao import DAO
from dotenv import dotenv_values
from src.util.validators import getValidator

@pytest.mark.daocreate
class TestDAO:
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
                        "nonRequiredString":{
                            "bsonType": "string",
                            "description": "Non-required string for test",
                        },
                        "testBool":{
                            "bsonType": "bool",
                            "description": "bool for test",
                        }
                    }
                }
            }
    #Overwrite DAO init with mocked version to use test_db insted of prod db
    @staticmethod
    def mocked_init(self):
        print("Runnig init")
        # load the local mongo URL (something like mongodb://localhost:27017)
        LOCAL_MONGO_URL = dotenv_values('.env').get('MONGO_URL')
        # check out of the environment (which can be overridden by the docker-compose file) also specifies an URL, and use that instead if it exists
        MONGO_URL = os.environ.get('MONGO_URL', LOCAL_MONGO_URL)

        # connect to the MongoDB and select the appropriate database
        print(
            f'Connecting to collection test on MongoDB at url {MONGO_URL}')
        client = pymongo.MongoClient(MONGO_URL)
        database = client.test_db

        # create the collection if it does not yet exist
        if "test" not in database.list_collection_names():
            validator = getValidator("test")
            database.create_collection("test", validator=validator)

        self.collection = database["test"]
    


    def test_1(self):
        with patch.object(DAO, '__init__', side_effect=self.mocked_init):
            obj = DAO("test")

            with patch('DAO.getValidator', return_value=self.validator):
                print(obj.validator)
                obj.dao.find.return_value = []

                assert None == None

    