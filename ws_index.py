import asyncio
import websockets
import gzip


async def hello():
    uri = "wss://api.hadax.com/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send("{\"sub\": \"market.ethbtc.kline.1min\",\"id\": \"id1\"}")
        async for message in websocket:
            print(gzip.compress(message).decode('utf8'))

asyncio.get_event_loop().run_until_complete(hello())
