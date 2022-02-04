from django.core.management.base import BaseCommand
from Market.models import Crawl_Info, Goods, Goods_Option
class Command(BaseCommand):
    
    
    def handle(self,  *args, **kwargs):
        Crawl_Info.objects.all().delete()