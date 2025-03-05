import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from websockets import connect
from django.core.cache import cache  
from channels.db import database_sync_to_async

class BinanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "binance_prices"
        # Dynamically fetch pair_name from URL
        self.pair_name = self.scope['url_route']['kwargs']['pair_name']
        self.url = f"wss://stream.binance.com:9443/ws/{self.pair_name.replace('/', '').lower()}@trade"

        # Add the client to the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Check if price is cached in Redis
        cached_price = cache.get(f'price_{self.pair_name}')
        if cached_price:
            # If cached price exists, send it to the client immediately
            await self.send(text_data=json.dumps({"price": cached_price}))

        try:
            self.binance_ws = await asyncio.wait_for(self.get_binance_data(), timeout=130)  
        except asyncio.TimeoutError:
            print("WebSocket connection timed out.")
            await self.close()

    async def disconnect(self, close_code):
        # Discard the client from the group and cancel the WebSocket task
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        if hasattr(self, 'binance_ws') and self.binance_ws:
            self.binance_ws.cancel()

    async def get_binance_data(self):
        try:
            async with connect(self.url) as ws:
                while True:
                    try:
                        data = json.loads(await ws.recv())
                        price = float(data['p'])

                        # Save the price in the DB
                        await self.save_price(self.pair_name, price)

                        # Cache the latest price in Redis (cache for 5 minutes)
                        cache.set(f'price_{self.pair_name}', price, timeout=60*5)

                        # Send the price to WebSocket clients
                        await self.channel_layer.group_send(
                            self.group_name,
                            {"type": "send_price", "price": price}
                        )
                    except json.JSONDecodeError:
                        print("Failed to decode WebSocket message.")
                    except KeyError:
                        print("Missing 'p' key in WebSocket data.")
                    except Exception as e:
                        print(f"WebSocket data error: {e}")
        except Exception as e:
            print(f"WebSocket error: {e}")

    async def save_price(self, pair_name, price):
        from .models import CryptoPrice
        try:
            # Save the price to the database
            await database_sync_to_async(CryptoPrice.objects.create)(pair_name=pair_name, price=price)
            print(f"Saved {pair_name} price: {price}")  # Log success
        except Exception as e:
            print(f"Error saving price: {e}")  # Log any errors


    async def send_price(self, event):
        # Send the price data to WebSocket clients
        await self.send(text_data=json.dumps({
            "price": event["price"]
        }))
