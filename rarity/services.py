import asyncio, requests, os, json
from aiohttp import ClientSession
from aiolimiter import AsyncLimiter
from django.core.exceptions import ValidationError
from django.conf import settings

config = settings.CONFIG

headers = {'project_id': config['BLOCKFROST_API_KEY']}

def fetch_all_assets(policy_id, num_pages=None):
    num_pages = num_pages if num_pages else fetch_num_pages(policy_id)
    async def coroutine():
        limiter = AsyncLimiter(500, 10)
        async with ClientSession(raise_for_status=True) as session:
            tasks = []
            for page in range(1, num_pages + 1):
                tasks.append(fetch_assets_on_page(page, session, policy_id, limiter))
            page_list = await asyncio.gather(*tasks)

            tasks = []
            for page in page_list:
                for asset in page:
                    tasks.append(fetch_metadata(asset['asset'], session, limiter))
            asset_list = await asyncio.gather(*tasks)
            return asset_list
    return asyncio.run(coroutine())


# fetch metadata for a given asset
async def fetch_metadata(asset_hex, session, limiter):
    url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/{asset_hex}'
    async with limiter:
        # print(f'Fetching {asset_hex}...')
        asset_metadata = await session.get(url, headers=headers)
        assert asset_metadata.status == 200
        return await asset_metadata.json(content_type=None)


# returns list of assets on page
async def fetch_assets_on_page(page, session, policy_id, limiter):
    url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/policy/{policy_id}'
    # print(f'Fetching assets on page {page}...')
    async with limiter:
        page_of_assets = await session.get(url=url, headers=headers, params={'page': page})
        return await page_of_assets.json()


def fetch_num_pages(policy_id, low=1, high=None, page=1):
    print(f'Determining number of pages...')
    url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/policy/{policy_id}'

    # fetch upperbound
    while high == None:
        r = requests.get(url, headers=headers, params={'page': page})
        if r.json():
            low = page
            page *= 2
        else:
            high = page
    # binary search for num_pages
    current_page = requests.get(url, {'page': page}, headers=headers).json()
    if current_page:
        next_page = requests.get(url, {'page': page + 1}, headers=headers).json()
        if not next_page:
            return page
        else:
            low = page + 1
            return fetch_num_pages(policy_id, low, high, (low + high) // 2)
    else:
        high = page
        return fetch_num_pages(policy_id, low, high, (low + high) // 2)


def flatten_metadata(metadata):
    res = {}
    def flatten(obj, name=''):
        if type(obj) is dict:
            for key in obj:
                flatten(obj[key], name + key + '_')
        elif type(obj) is list:
            res[name[:-1]] = obj

        else:
            res[name[:-1]] = obj

    flatten(metadata)
    return res


def validate_policy_id(policy_id):
    url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/policy/{policy_id}'
    r = requests.get(url, {'page': 1}, headers=headers)
    if r.status_code == 404:
        raise ValidationError(f'Invalid policy_id: {policy_id}')















