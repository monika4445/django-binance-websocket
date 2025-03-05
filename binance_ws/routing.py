from django.urls import path
from .consumers import BinanceConsumer

from django.urls import re_path
from .consumers import BinanceConsumer

websocket_urlpatterns = [
    re_path(r"ws/binance/(?P<pair_name>\w{3,5}/\w{3,5})/", BinanceConsumer.as_asgi()),
]
