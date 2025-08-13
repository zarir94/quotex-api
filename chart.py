from pyquotex.stable_api import Quotex
import asyncio

async def main():
    client = Quotex(email="mariamkhanam1979@gmail.com", password="mariam@1", lang="en")
    success, message = await client.connect()
    if success:
        print(f'Connected, {message}')
    else:
        print(f'Failed, {message}')


asyncio.run(main())

