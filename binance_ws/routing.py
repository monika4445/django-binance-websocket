from django.urls import path
from .consumers import BinanceConsumer

websocket_urlpatterns = [
    path("ws/binance/", BinanceConsumer.as_asgi()),
]

