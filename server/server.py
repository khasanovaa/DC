import tornado.ioloop
import tornado.web
import json

def print_elem(elem):
    return str(elem)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear()
        self.set_status(400)
        self.finish("<html><body>Hello!</body></html>")

elements = {}

class ShowAllHandler(tornado.web.RequestHandler):
    def get(self):
        ans = ''
        for elem in elements:
            ans = ans + print_elem(elements[elem]) + '\n'
        self.write(ans)

class CreateHandler(tornado.web.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        if (not body.get('id') or not body.get('name') or not body.get('category')):
            self.clear()
            self.set_status(400)
            self.finish("<html><body>Wrong arguments</body></html>")
        elif elements.get(body['id']):
            self.clear()
            self.set_status(400)
            self.finish("<html><body>There is already element with this id. Try to use update method.</body></html>")
        else:
            self.set_status(200)
            elements[body['id']] = body

class DeleteHandler(tornado.web.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        if (not body.get('id')):
            self.clear()
            self.set_status(400)
            self.finish("<html><body>Wrong arguments</body></html>")
        id = body['id']
        if (not elements.get(id)):
            self.clear()
            self.set_status(400)
            self.finish("<html><body>No element with this id.</body></html>")
        elements.pop(id)

class ShowOneHandler(tornado.web.RequestHandler):
    def get(self):
        body = json.loads(self.request.body)
        if (not body.get('id')):
            self.clear()
            self.set_status(400)
            self.finish("<html><body>Wrong arguments</body></html>")
        id = body['id']
        if (not elements.get(id)):
            self.clear()
            self.set_status(400)
            self.finish("<html><body>No element with this id.</body></html>")
        self.set_status(200)
        self.write(print_elem(elements[id]) + '\n')

class UpdateHandler(tornado.web.RequestHandler):
    def post(self):
        body = json.loads(self.request.body)
        if (not body.get('id')):
            self.clear()
            self.set_status(400)
            self.finish("<html><body>Wrong arguments</body></html>")
        id = body['id']
        if (body.get('name')):
            elements[id]['name'] = body['name']
        if (body.get('category')):
            elements[id]['category'] = body['category']

def make_app():
    return tornado.web.Application([
        (r"/create", CreateHandler),
        (r"/showall", ShowAllHandler),
        (r"/delete", DeleteHandler),
        (r"/showone", ShowOneHandler),
        (r"/update", UpdateHandler),
        (r"/", MainHandler),

    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()