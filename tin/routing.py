from typing import Optional

from channels.auth import AuthMiddlewareStack
from channels.generic.websocket import WebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import path

from .apps.submissions.consumers import SubmissionJsonConsumer


class WebsocketCloseConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.close()

    def receive(self, text_data: Optional[str] = None, bytes_data: Optional[bytes] = None):
        pass

    def disconnect(self, code):
        pass


application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    path("submissions/<int:submission_id>.json", SubmissionJsonConsumer),
                    path("<path:path>", WebsocketCloseConsumer),
                ]
            )
        )
    }
)
