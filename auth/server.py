import tornado.ioloop
import tornado.web
import json
from Database import DataBase
from authconfig import AUTH_PORT

def print_elem(elem):
    return str(elem)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear()
        self.set_status(200)
        response = {'status': 'ok'}
        self.finish(response)


db = DataBase()

class Signup(tornado.web.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        if (not body.get('login') or not body.get('password')):
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details' : 'Wrong arguments'}
            self.finish(response)
            return

        try:
            db.signup(body)
            self.clear()
            self.set_status(200)
            response = {'status': 'ok'}
            self.finish(response)
        except Exception as e:
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details': '{}'.format(e)}
            self.finish(response)

class Signin(tornado.web.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        if (not body.get('login') or not body.get('password')):
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details' : 'Wrong arguments'}
            self.finish(response)
            return

        try:
            self.clear()
            self.set_status(200)
            tokens = db.signin(body)
            response = {'status': 'ok', 'info': db.signin(body)}
            self.finish(response)
        except Exception as e:
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details': '{}'.format(e)}
            self.finish(response)

class Validate(tornado.web.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        if (not body.get('access_token')):
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details' : 'Wrong arguments'}
            self.finish(response)
            return
        response = db.validate(body)
        if (response['result']):
            self.clear()
            self.set_status(200)
            response = {'status': 'ok'}
            self.finish(response)
        else:
            self.clear()
            self.set_status(200)
            response = {'status': 'error', 'details': response['details']}
            self.finish(response)

class Refresh(tornado.web.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        if (not body.get('refresh_token')):
            self.clear()
            self.set_status(400)
            response = {'status': 'error', 'details' : 'Wrong arguments'}
            self.finish(response)
            return

        response = db.refresh(body)
        if (response['result']):
            self.clear()
            self.set_status(200)
            response = {'status': 'ok', 'details': response['details']}
            self.finish(response)
        else:
            self.clear()
            self.set_status(200)
            response = {'status': 'error', 'details': response['details']}
            self.finish(response)


def make_app():
    return tornado.web.Application([
        (r"/signup", Signup),
        (r"/signin", Signin),
        (r"/refresh", Refresh),
        (r"/validate", Validate),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(AUTH_PORT)
    tornado.ioloop.IOLoop.current().start()