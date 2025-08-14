from pyquotex.stable_api import Quotex
import asyncio, os

os.environ['QX_HTTPS_BASE'] = 'https://market-qx.trade'


async def main():
    client = Quotex('drive4341@gmail.com', 'drive@1', 'en')
    await client.connect()
    candles = await client.get_candle_v2('EURUSD', 60)
    print(len(candles))


asyncio.run(main())


