import json
import websockets
import asyncio
from .models import CryptoPrice
from asgiref.sync import sync_to_async

class BinanceService:
    BINANCE_WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"

    @staticmethod
    async def fetch_binance_data():
        async with websockets.connect(BinanceService.BINANCE_WS_URL) as ws:
            while True:
                data = json.loads(await ws.recv())
                price = float(data['p'])
                await sync_to_async(CryptoPrice.objects.create)(symbol="BTC/USDT", price=price)
                print(f"Saved price: {price}")

    @staticmethod
    def start_background_task():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(BinanceService.fetch_binance_data())
