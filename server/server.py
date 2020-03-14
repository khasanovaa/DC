import tornado.ioloop
import tornado.web
import json
from Database import DataBase


def print_elem(elem):
    return str(elem)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear()
        self.set_status(200)
        response = {'status': 'ok'}
        self.finish(response)


db = DataBase()


class Items(tornado.web.RequestHandler):
    def get(self):
        self.write({'items': db.get_items(), 'status': 'ok'})


class Item(tornado.web.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        if (not body.get('id') or not body.get('name') or not body.get('category')):
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details' : 'Wrong arguments'}
            self.finish(response)
        else:
            try:
                db.insert(body)
                self.clear()
                self.set_status(200)
                response = {'status': 'ok'}
                self.finish(response)
            except Exception as e:
                self.clear()
                self.set_status(400)
                response = {'status': 'error', 'details': 'Error while creating element: {}'.format(e)}
                self.finish(response)

    def delete(self):
        body = json.loads(self.request.body)
        if (not body.get('id')):
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details': 'Wrong arguments'}
            self.finish(response)
            return

        id = body['id']
        try:
            db.delete(id)
            self.clear()
            self.set_status(200)
            response = {'status': 'ok'}
            self.finish(response)
        except Exception as e:
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details': '{}'.format(e)}
            self.finish(response)

    def get(self):
        body = json.loads(self.request.body)
        if (not body.get('id')):
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details': 'Wrong arguments'}
            self.finish(response)
            return
        id = body['id']
        try:
            res = db.find(id)
            self.set_status(200)
            response = {'status': 'ok', 'items:': res}
            self.finish(response)
            return
        except Exception as e:
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details': '{}'.format(e)}
            self.finish(response)

    def put(self):
        body = json.loads(self.request.body)
        if not body.get('id'):
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details': 'Wrong arguments'}
            self.finish(response)
            return
        id = body.pop('id')
        try:
            db.update(id, body)
            self.set_status(200)
            response = {'status': 'ok'}
            self.finish(response)
            return
        except Exception as e:
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details': '{}'.format(e)}
            self.finish(response)


def make_app():
    return tornado.web.Application([
        (r"/item", Item),
        (r"/items", Items),
        (r"/", MainHandler),

    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()