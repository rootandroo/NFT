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
        collections = Collection.objects.all()
        
        market_data = fetch_mrkt_data(collections)

        for page in market_data:
            for asset_data in page['assets']:
                id = asset_data['id']
                price = asset_data['price']
                name = asset_data['metadata']['name']
                try:
                    asset = Asset.objects.get(onchain_metadata__name=name)    
                    asset.market = {}
                    asset.market[market] = {}
                    asset.market[market]['price'] = price
                    asset.market[market]['id'] = id
                    asset.save()
                except ObjectDoesNotExist:
                    logger.warn(f'Asset with name: {name} does not exist.')