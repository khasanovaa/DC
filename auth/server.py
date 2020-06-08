import tornado.ioloop
import tornado.web
import json
from Database import DataBase
from authconfig import AUTH_PORT
import pika
import secrets

def print_elem(elem):
    return str(elem)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear()
        self.set_status(200)
        response = {'status': 'ok'}
        self.finish(response)


db = DataBase()

def SendEmail(email):
    credentials = pika.PlainCredentials('user', 'user')
    parameters = pika.ConnectionParameters('rabbitmq',
                                           5672,
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    token = secrets.token_hex(64)
    link = "http://localhost:8080/confirm?token=" + str(token)
    print(link, flush=True)
    message = 'Subject: {}\n\n{}'.format("Please, confirm your email address", str(link))
    data = {'message':message, 'email':email}
    channel.basic_publish(exchange='',
                          routing_key='hello',
                              body=json.dumps(data))
    return token

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
            token = SendEmail(body.get('login'))
            db.addtoken({'token':token, 'login': body.get('login')})
            response = {'status': 'Verify your email'}
            self.clear()
            self.set_status(200)
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

class Confirm(tornado.web.RequestHandler):
    def get(self):
        token = self.get_query_argument("token")
        response = db.confirm({'token': token})
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
        (r"/confirm", Confirm),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(AUTH_PORT)
    tornado.ioloop.IOLoop.current().start()