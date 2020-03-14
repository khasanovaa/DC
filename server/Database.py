from tinydb import TinyDB, Query


class DataBase:
    def __init__(self):
        self.db = TinyDB('./db.json')
        self.table = self.db.table('items')

    def insert(self, doc):
        id = doc['id']
        existing_items = self.get_items(id)
        if len(existing_items) != 0:
            raise Exception('Item with id {} ALREADY EXISTS'.format(id))
        self.table.insert(doc)

    def delete(self, id):
        item = Query()
        self.find(id)  # Checking, that item exists.
        self.table.remove(item.id == id)

    def update(self, id, doc):
        item = Query()
        existing_item = self.find(id)
        existing_item.update(doc)
        self.table.update(existing_item, item.id == id)

    def get_items(self, id=None):
        item = Query()
        if id is None:
            return self.table.all()
        return self.table.search(item.id == id)

    def find(self, id):
        item = Query()
        existing_items = self.table.search(item.id == id)
        if len(existing_items) != 1:
            raise Exception('Item with id {} NOT FOUND'.format(id))
        return existing_items[0]

    def close(self):
        self.db.close()
