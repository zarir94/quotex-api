from pyquotex.stable_api import Quotex
import asyncio, os, requests as rq, logging

# logging.basicConfig(level=logging.DEBUG)

# os.environ['QX_HTTPS_BASE'] = '/'.join(rq.get('https://qxbroker.com', verify=False).url.split('/', 3)[:3])


async def main():
    client = Quotex('drive4341@gmail.com', 'drive@1', 'en')
    await client.connect()
    assets = dict()
    for i, j in client.get_all_asset_name():
        assets[j] = i
    print(assets)
    

asyncio.run(main())


