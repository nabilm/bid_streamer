""" Mongodb helper using async IO motor client """

import motor.motor_asyncio


class MongoClient:
    """ A mongo client to specific DB """

    dsn: str
    db_name: str

    def __init__(self, dsn: str, db):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(dsn)
        self.db = self._client[db]

    async def do_insert_one(self, collection_name: str, document):
        col = self.db[collection_name]
        result = await col.insert_one(document)
        return result.inserted_id

    async def do_insert_many(self, collection_name: str, documents: list):
        col = self.db[collection_name]
        result = await col.insert_many(documents)
        return result.inserted_ids

    async def do_find(self, collection_name: str, query: dict, len: str = 100):
        col = self.db[collection_name]
        # We want the default to hide mongodb object id because
        # we don't want to rely on it that make the db scheme independent
        init_query = {"_id": False}
        cursor = col.find(query, init_query)
        result = await cursor.to_list(length=100)
        return result

    async def do_find_one(self, collection_name: str, query: dict):
        col = self.db[collection_name]
        init_query = {"_id": False}
        result = await col.find_one(query, init_query)
        return result

    async def do_update_one(self, collection_name: str, id: str, query):
        col = self.db[collection_name]
        result = col.update_one({"id": id}, query)
        return result
