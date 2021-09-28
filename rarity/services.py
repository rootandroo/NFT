import asyncio, requests, os, re
from aiohttp import ClientSession
from rarity.models import Asset
from aiolimiter import AsyncLimiter


headers = {'project_id': 'WAt3iqJeKl7mwX9mLEesc51Sjvptn114'}


def fetch_all_assets(policy_id):
    async def coroutine():
        limiter = AsyncLimiter(500, 10)
        num_pages = fetch_num_pages(policy_id)
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
        print(f'Fetching {asset_hex}...')
        asset_metadata = await session.get(url, headers=headers)
        assert asset_metadata.status == 200
        return await asset_metadata.json(content_type=None)


# returns list of assets on page
async def fetch_assets_on_page(page, session, policy_id, limiter):
    url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/policy/{policy_id}'
    print(f'Fetching assets on page {page}...')
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


def create_asset_objs(asset_list, collection):
    objs = []
    for asset in asset_list:
        objs.append(Asset(
            name=asset['asset_name'],
            policy_id=asset['policy_id'],
            fingerprint=asset['fingerprint'],
            quantity=asset['quantity'],
            mint_tx_hash=asset['initial_mint_tx_hash'], 
            onchain_metadata=asset['onchain_metadata'],
            collection=collection))
    return objs


def get_num(hex):
    # hex to str
    bytes_obj = bytes.fromhex(hex)
    string = bytes_obj.decode('ASCII')
    match = re.findall('\d+$', string)
    return int(match[0])

    
def is_policy_id(policy_id):
    url = f'https://cardano-mainnet.blockfrost.io/api/v0/assets/policy/{policy_id}'
    r = requests.get(url, {'page': 1}, headers=headers)
    return r.status_code != 404