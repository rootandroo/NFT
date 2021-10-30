from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from rarity.models import Collection, Asset
from rarity.services import fetch_col_mrkt_data
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Updates market data for Assets in all Collections"

    def handle(self, *args, **kwargs):
        mrkt = "CNFTio"
        collections = Collection.objects.all()
        for col in collections:
            logger.warn(f'Fetching {col} from {mrkt}.')

            col_mrkt_data = fetch_col_mrkt_data(col)
            for page in col_mrkt_data:
                for asset_data in page['assets']:
                    id = asset_data['id']
                    price = asset_data['price']
                    name = asset_data['metadata']['name']
                    try:
                        asset = Asset.objects.get(onchain_metadata__name=name)    
                        asset.market = {}
                        asset.market[mrkt] = {}
                        asset.market[mrkt]['price'] = price
                        asset.market[mrkt]['id'] = id
                        asset.save()
                    except ObjectDoesNotExist:
                        logger.warn(f'Asset with name: {name} does not exist.')