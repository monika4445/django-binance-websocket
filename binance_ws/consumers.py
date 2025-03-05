# binance_ws/consumers.py
import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from websockets import connect

class BinanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "binance_prices"
        # Add the client to the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        # Start listening to the Binance WebSocket
        self.binance_ws = asyncio.create_task(self.get_binance_data())

    async def disconnect(self, close_code):
        # Discard the client from the group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        if self.binance_ws:
            self.binance_ws.cancel()

    async def get_binance_data(self):
        url = "wss://stream.binance.com:9443/ws/btcusdt@trade"
        try:
            async with connect(url) as ws:
                while True:
                    data = json.loads(await ws.recv())
                    price = float(data['p'])
                    # You can add logic to save to the database here if needed
                    
                    # Broadcast the data to the WebSocket group
                    await self.channel_layer.group_send(
                        self.group_name,
                        {"type": "send_price", "price": price}
                    )
        except Exception as e:
            print(f"WebSocket error: {e}")

    async def send_price(self, event):
        # Send the price data to the WebSocket client
        await self.send(text_data=json.dumps({
            "price": event["price"]
        }))
