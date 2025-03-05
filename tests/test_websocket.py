import pytest
from channels.testing import WebsocketCommunicator
from binance_ws.consumers import BinanceConsumer

@pytest.mark.asyncio
async def test_binance_consumer():
    communicator = WebsocketCommunicator(BinanceConsumer.as_asgi(), "/ws/binance/")
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()
