import aiohttp
import asyncio
import time
import httpx
import json
import sys

#test data
contracts = [
'0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3',
'0xddae277e4ebb71715fb4221b9e7a2d8986d641cf',
'0xed2c17dbbce2d8ae976a1534a1e537db0138ecdd',
'0x69c5240efd9a1538aedc532993a8fa7da12b54ca',
'0x4e6415a5727ea08aae4580057187923aec331227',
'0x40986a85b4cfcdb054a6cbfb1210194fee51af88',
'0x27ae27110350b98d564b9a3eed31baebc82d878d',
'0x5e90253fbae4dab78aa351f4e6fed08a64ab5590',
'0xe4ab812613f03d2b00d34bfa43f1b7cf211a10d7',
'0x0523215dcafbf4e4aa92117d13c6985a3bef27d7',
'0x31de61d9a39cb9f479570bd3dc3ac93bc0402cdb',
'0x954be3e377661a2b01841e487ca294c4204dbb79',
'0xef032f652fce3a0effce3796a68eb978b465a336',
'0xbcbcd3fdc07d496d1145f41a65a3e957efed9946',
'0x0e3eaf83ea93abe756690c62c72284943b96a6bc',
'0xf565aaf0b8eb813a1c8c956d2c59f1ce27fd2366',
'0xa58950f05fea2277d2608748412bf9f802ea4901',
'0x0952ddffde60786497c7ced1f49b4a14cf527f76',
'0x3540e2e9b59b65d891ed308c466b30cb8e9740ce',
'0x5610bf2bf5abe5750bdbce311631dee2afa2cd24',
'0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3',
'0xddae277e4ebb71715fb4221b9e7a2d8986d641cf',
'0xed2c17dbbce2d8ae976a1534a1e537db0138ecdd',
'0x69c5240efd9a1538aedc532993a8fa7da12b54ca',
'0x4e6415a5727ea08aae4580057187923aec331227',
'0x40986a85b4cfcdb054a6cbfb1210194fee51af88',
'0x27ae27110350b98d564b9a3eed31baebc82d878d',
'0x5e90253fbae4dab78aa351f4e6fed08a64ab5590',
'0xe4ab812613f03d2b00d34bfa43f1b7cf211a10d7',
'0x0523215dcafbf4e4aa92117d13c6985a3bef27d7',
'0x31de61d9a39cb9f479570bd3dc3ac93bc0402cdb',
'0x954be3e377661a2b01841e487ca294c4204dbb79',
'0xef032f652fce3a0effce3796a68eb978b465a336',
'0xbcbcd3fdc07d496d1145f41a65a3e957efed9946',
'0x0e3eaf83ea93abe756690c62c72284943b96a6bc',
'0xf565aaf0b8eb813a1c8c956d2c59f1ce27fd2366',
'0xa58950f05fea2277d2608748412bf9f802ea4901',
'0x0952ddffde60786497c7ced1f49b4a14cf527f76',
'0x3540e2e9b59b65d891ed308c466b30cb8e9740ce',
'0x5610bf2bf5abe5750bdbce311631dee2afa2cd24',
'0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3',
'0xddae277e4ebb71715fb4221b9e7a2d8986d641cf',
'0xed2c17dbbce2d8ae976a1534a1e537db0138ecdd',
'0x69c5240efd9a1538aedc532993a8fa7da12b54ca',
'0x4e6415a5727ea08aae4580057187923aec331227',
'0x40986a85b4cfcdb054a6cbfb1210194fee51af88',
'0x27ae27110350b98d564b9a3eed31baebc82d878d',
'0x5e90253fbae4dab78aa351f4e6fed08a64ab5590',
'0xe4ab812613f03d2b00d34bfa43f1b7cf211a10d7',
'0x0523215dcafbf4e4aa92117d13c6985a3bef27d7',
'0x31de61d9a39cb9f479570bd3dc3ac93bc0402cdb',
'0x954be3e377661a2b01841e487ca294c4204dbb79',
'0xef032f652fce3a0effce3796a68eb978b465a336',
'0xbcbcd3fdc07d496d1145f41a65a3e957efed9946',
'0x0e3eaf83ea93abe756690c62c72284943b96a6bc',
'0xf565aaf0b8eb813a1c8c956d2c59f1ce27fd2366',
'0xa58950f05fea2277d2608748412bf9f802ea4901',
'0x0952ddffde60786497c7ced1f49b4a14cf527f76',
'0x3540e2e9b59b65d891ed308c466b30cb8e9740ce',
'0x5610bf2bf5abe5750bdbce311631dee2afa2cd24',
'0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3',
'0xddae277e4ebb71715fb4221b9e7a2d8986d641cf',
'0xed2c17dbbce2d8ae976a1534a1e537db0138ecdd',
'0x69c5240efd9a1538aedc532993a8fa7da12b54ca',
'0x4e6415a5727ea08aae4580057187923aec331227',
'0x40986a85b4cfcdb054a6cbfb1210194fee51af88',
'0x27ae27110350b98d564b9a3eed31baebc82d878d',
'0x5e90253fbae4dab78aa351f4e6fed08a64ab5590',
'0xe4ab812613f03d2b00d34bfa43f1b7cf211a10d7',
'0x0523215dcafbf4e4aa92117d13c6985a3bef27d7',
'0x31de61d9a39cb9f479570bd3dc3ac93bc0402cdb',
'0x954be3e377661a2b01841e487ca294c4204dbb79',
'0xef032f652fce3a0effce3796a68eb978b465a336',
'0xbcbcd3fdc07d496d1145f41a65a3e957efed9946',
'0x0e3eaf83ea93abe756690c62c72284943b96a6bc',
'0xf565aaf0b8eb813a1c8c956d2c59f1ce27fd2366',
'0xa58950f05fea2277d2608748412bf9f802ea4901',
'0x0952ddffde60786497c7ced1f49b4a14cf527f76',
'0x3540e2e9b59b65d891ed308c466b30cb8e9740ce',
'0x5610bf2bf5abe5750bdbce311631dee2afa2cd24',
'0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3',
'0xddae277e4ebb71715fb4221b9e7a2d8986d641cf',
'0xed2c17dbbce2d8ae976a1534a1e537db0138ecdd',
'0x69c5240efd9a1538aedc532993a8fa7da12b54ca',
'0x4e6415a5727ea08aae4580057187923aec331227',
'0x40986a85b4cfcdb054a6cbfb1210194fee51af88',
'0x27ae27110350b98d564b9a3eed31baebc82d878d',
'0x5e90253fbae4dab78aa351f4e6fed08a64ab5590',
'0xe4ab812613f03d2b00d34bfa43f1b7cf211a10d7',
'0x0523215dcafbf4e4aa92117d13c6985a3bef27d7',
'0x31de61d9a39cb9f479570bd3dc3ac93bc0402cdb',
'0x954be3e377661a2b01841e487ca294c4204dbb79',
'0xef032f652fce3a0effce3796a68eb978b465a336',
'0xbcbcd3fdc07d496d1145f41a65a3e957efed9946',
'0x0e3eaf83ea93abe756690c62c72284943b96a6bc',
'0xf565aaf0b8eb813a1c8c956d2c59f1ce27fd2366',
'0xa58950f05fea2277d2608748412bf9f802ea4901',
'0x0952ddffde60786497c7ced1f49b4a14cf527f76',
'0x3540e2e9b59b65d891ed308c466b30cb8e9740ce',
'0x5610bf2bf5abe5750bdbce311631dee2afa2cd24',
'0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3',
'0xddae277e4ebb71715fb4221b9e7a2d8986d641cf',
'0xed2c17dbbce2d8ae976a1534a1e537db0138ecdd',
'0x69c5240efd9a1538aedc532993a8fa7da12b54ca',
'0x4e6415a5727ea08aae4580057187923aec331227',
'0x40986a85b4cfcdb054a6cbfb1210194fee51af88',
'0x27ae27110350b98d564b9a3eed31baebc82d878d',
'0x5e90253fbae4dab78aa351f4e6fed08a64ab5590',
'0xe4ab812613f03d2b00d34bfa43f1b7cf211a10d7',
'0x0523215dcafbf4e4aa92117d13c6985a3bef27d7',
'0x31de61d9a39cb9f479570bd3dc3ac93bc0402cdb',
'0x954be3e377661a2b01841e487ca294c4204dbb79',
'0xef032f652fce3a0effce3796a68eb978b465a336',
'0xbcbcd3fdc07d496d1145f41a65a3e957efed9946',
'0x0e3eaf83ea93abe756690c62c72284943b96a6bc',
'0xf565aaf0b8eb813a1c8c956d2c59f1ce27fd2366',
'0xa58950f05fea2277d2608748412bf9f802ea4901',
'0x0952ddffde60786497c7ced1f49b4a14cf527f76',
'0x3540e2e9b59b65d891ed308c466b30cb8e9740ce',
'0x5610bf2bf5abe5750bdbce311631dee2afa2cd24',
'0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3',
'0xddae277e4ebb71715fb4221b9e7a2d8986d641cf',
'0xed2c17dbbce2d8ae976a1534a1e537db0138ecdd',
'0x69c5240efd9a1538aedc532993a8fa7da12b54ca',
'0x4e6415a5727ea08aae4580057187923aec331227',
'0x40986a85b4cfcdb054a6cbfb1210194fee51af88',
'0x27ae27110350b98d564b9a3eed31baebc82d878d',
'0x5e90253fbae4dab78aa351f4e6fed08a64ab5590',
'0xe4ab812613f03d2b00d34bfa43f1b7cf211a10d7',
'0x0523215dcafbf4e4aa92117d13c6985a3bef27d7',
'0x6884ae24deb7e8fa80dc9d0d56c91d78a250e9b1'
]

headers = {
    'User-Agent': 'Mozilla'
}


def load_tokens_slow(ids):
    for id in ids:
        url = "https://api.dex.guru/v1/tokens/"+id+"-bsc"
        response = httpx.get(url)
        if response.status_code == 200:
            parsed = json.loads(response.text)
        
    return parsed


async def get_token(session, url):
    async with session.get(url, headers=headers) as resp:
        if resp.status == 200:
            token = await resp.json()
            return token


async def load_tokens(ids):

    async with aiohttp.ClientSession() as session:
        tasks = []
        for id in ids:
            url = "https://api.dex.guru/v1/tokens/"+id#+"-bsc"
            tasks.append(asyncio.ensure_future(get_token(session, url)))

        tokens = await asyncio.gather(*tasks)
        return tokens

async def load_tokens_async(ids):

    async with aiohttp.ClientSession() as session:
        parsed = dict()
        for id in ids:
            url = "https://api.dex.guru/v1/tokens/"+id+"-bsc"
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    parsed = await resp.json()
        return parsed

def load(ids):
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    try:
        return asyncio.get_event_loop().run_until_complete(load_tokens(ids))
    except Exception as e:
        print(e, file=sys.stderr)


if __name__ == '__main__':

    start_time = time.time()
    load(contracts)
    print("--- async optimized %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(load_tokens_async(contracts))
    print("--- async %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    load_tokens_slow(contracts)
    print("--- normal %s seconds ---" % (time.time() - start_time))
