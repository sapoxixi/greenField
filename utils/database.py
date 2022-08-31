import motor.motor_asyncio as motor
import asyncio
import traceback

USER = "XXXXXXXX"
PASSWORD = 'XXXXXXXX'
uri = 'XXXXXXXX'
DATABASE = 'field'
COLLECTION = 'species'

class Database():
    """Implements the client and helpful fun to be used by the states"""

    def __init__(self):
        self.cluster = motor.AsyncIOMotorClient(uri)
        self.db = self.cluster[DATABASE]
        self.collection = self.db[COLLECTION]

        self.cluster.get_io_loop = asyncio.get_running_loop

    async def insert_or_update(self, data, find_keys):
        """Inserts data into db or update if the given name already exists"""

        try:
            find_dict = self.get_find_dict(data, find_keys)

            await asyncio.sleep(3)
            if await self.find_one(find_dict):
                to_update_dict = self.get_find_dict(data, find_keys)
                update_dict = self.get_update_dict(data, find_keys)

                await self.update_one(to_update_dict, update_dict)
                return None
            else:
                inserted_id = await self.collection.insert_one(data)
        except:
            print('Something went wrong when inserting in database: \n')
            traceback.print_exc() 
            return None
        
        return inserted_id.inserted_id

    async def find_all_by_dict(self, find_dict):
        """Find all documents by the given dict with the key(s) and value(s)"""

        try:
            found = self.collection.find(find_dict)
        except:
            print('Something went wrong when finding all in database: \n')
            traceback.print_exc() 
            return None
        
        await asyncio.sleep(3)
        found_list = []
        async for item in found:
            item.pop('_id')
            found_list.append(item)
        
        return found_list

    async def find_one(self, data):
        found = await self.collection.find_one(data)

        return found
    
    def get_find_dict(self, data, find_keys):
        find_dict = {}
        for key in find_keys:
            find_dict[key] = data[key]
        return find_dict

    def get_update_dict(self, data, find_keys):
        for to_del in find_keys:
            data.pop(to_del)

        return data

    async def update_one(self, updated, update_dict):
        self.collection.update_one(updated, {'$set': update_dict})

    async def clear_by_dict(self, clear_dict):
        """Delete all documents by the given dict with the key(s) and value(s)"""

        try:
            await asyncio.sleep(1)
            cleared = await self.collection.delete_many(clear_dict)
        except:
            print('Something went wrong when clearing by ' + str(clear_dict) + '\n')
            traceback.print_exc() 
            return None
        
        return cleared.deleted_count
