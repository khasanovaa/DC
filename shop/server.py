import tornado.ioloop
import tornado.web
import json
from Database import DataBase
import requests
from config import SERVER_PORT
from authconfig import AUTH_HOST, AUTH_PORT
db = DataBase()

def validate(access_token):
    body = body = json.dumps({'access_token': access_token})
    response = requests.post('http://{}:{}/validate'.format(AUTH_HOST, AUTH_PORT), data= body)
    response_data = response.json()
    if response_data['status'] != 'ok':
        raise Exception('User is not authorized. Invalid access token.')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear()
        self.set_status(200)
        response = {'status': 'ok'}
        self.finish(response)


class Items(tornado.web.RequestHandler):
    def get(self):
        self.write({'status': 'ok', 'items': db.get_items()})


class Item(tornado.web.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        if (not body.get('id') or not body.get('name') or not body.get('category')):
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details' : 'Wrong arguments'}
            self.finish(response)
            return
        else:
            try:
                access_token = self.request.headers["Authorization"]
                validate(access_token)
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
        id = self.get_query_argument("id")
        try:
            access_token = self.request.headers["Authorization"]
            validate(access_token)
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
        id = self.get_query_argument("id")
        try:
            res = db.find(id)
            self.set_status(200)
            response = {'status': 'ok', 'items:': res}
            self.finish(response)
        except Exception as e:
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details': '{}'.format(e)}
            self.finish(response)

    def put(self):
        body = json.loads(self.request.body)
        id = self.get_query_argument("id")
        try:
            access_token = self.request.headers['Authorization']
            validate(access_token)
            db.update(id, body)
            self.set_status(200)
            response = {'status': 'ok'}
            self.finish(response)
        except Exception as e:
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details': '{}'.format(e)}
            self.finish(response)


def make_app():
    return tornado.web.Application([
        (r"/items", Items),
        (r"/item", Item),
        # (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(SERVER_PORT)
    tornado.ioloop.IOLoop.current().start()