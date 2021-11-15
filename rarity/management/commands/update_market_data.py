from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from rarity.models import Collection, Asset
from rarity.services import fetch_mrkt_data
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Updates market data for Assets in all Collections"

    def handle(self, *args, **kwargs):
        market = "CNFTio"
        collections = list(Collection.objects.all())
        
        logger.info(f'Fetching market data...')

        market_data = fetch_mrkt_data(collections)

        logger.info(f'Finished fetching market data.')

        updated_objs = []        
        for page in market_data:
            names = [asset['asset']['assetId'] for asset in page["results"]]
            assets = Asset.objects.filter(decoded_name__in=names)
            for asset_data in page["results"]:
                id = asset_data['_id']
                price = asset_data['price']
                name = asset_data['asset']['assetId']
                try:
                    asset = assets.get(decoded_name=name)    
                    asset.market = {}
                    asset.market[market] = {}
                    asset.market[market]['price'] = price
                    asset.market[market]['id'] = id
                    updated_objs.append(asset)
                except ObjectDoesNotExist:
                    logger.warn(f'Asset with name: {name} does not exist.')
        Asset.objects.bulk_update(updated_objs, ['market'], batch_size=1000)
        logger.info(f'Updated all prices for new listings.')