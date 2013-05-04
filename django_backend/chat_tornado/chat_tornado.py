# -*- coding: utf-8 -*-
"""
    Simple sockjs-tornado chat application. By default will listen on port 8080.
"""
import tornado.ioloop
import tornado.web

import sockjs.tornado
import os
import sys

sys.path.append(os.path.abspath(os.path.join(__file__, '..', '..')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_backend.settings'
from chat.models import ChatLog


class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render('index.html')


class ChatConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    # Class level variable
    participants = set()

    def on_open(self, info):
        # Send that someone joined
        self.broadcast(self.participants, "Someone joined.")

        # Add client to the clients list
        self.participants.add(self)
        chat_log = ChatLog.objects.order_by('id')
        for chat in chat_log:
            self.send(chat.message)

    def on_message(self, message):
        # Broadcast message
        self.broadcast(self.participants, message)
        # message log to Django ORM
        ChatLog.objects.create(message=message)

    def on_close(self):
        # Remove client from the clients list and broadcast leave message
        self.participants.remove(self)

        self.broadcast(self.participants, "Someone left.")

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # 1. Create chat router
    ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/chat')

    # 2. Create Tornado application
    app = tornado.web.Application(
        [(r"/", IndexHandler)] + ChatRouter.urls
    )

    # 3. Make Tornado app listen on port 8080
    app.listen(8080)

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
