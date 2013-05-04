# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    """sample handler"""
    def get(self):
        self.write("Hello world")


class StoryHandler(tornado.web.RequestHandler):
    def get(self, story_id):
        self.write("story~" + story_id)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/story/(\d+)", StoryHandler),
])

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
