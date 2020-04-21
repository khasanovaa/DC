from pymongo import MongoClient
from config import MONGO_HOST, MONGO_PORT

class DataBase:
    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client.db
        self.table = self.db.items

    def insert(self, doc):
        id = doc['id']
        if (self.exists(id)):
            raise Exception('Item with id {} is ALREADY EXISTS'.format(id))
        self.table.insert_one(doc)

    def delete(self, id):
        if (not self.exists(id)):
            raise Exception('Item with id {} was NOT FOUND'.format(id))
        self.table.delete_one({'id': id})

    def update(self, id, doc):
        if (not self.exists(id)):
            raise Exception('Item with id {} was NOT FOUND'.format(id))
        name = doc['name']
        category = doc['category']
        self.table.update_one({'id': id}, {'$set': {'name': name, 'category': category}})

    def get_items(self):
        all_items = list(self.table.find({}))
        result = []
        for item in all_items:
            item.pop('_id')
            result.append(item)
        return result

    def find(self, id):
        if (not self.exists(id)):
            raise Exception('Item with id {} was NOT FOUND'.format(id))
        founded = self.table.find_one({'id': id})
        founded.pop('_id')
        return founded

    def exists(self, id):
        if self.table.find({'id': id}).count() > 0:
            return True
        else:
            return False
