from django.db import models
# from Skills.models import Equipments

class Crawl_Info(models.Model):
    crawl_uuid      = models.CharField(max_length = 40)
    serverid        = models.IntegerField(db_index=True)
    created         = models.DateTimeField(auto_now_add=True)
    def Goods(self):
        return self.goods_set.all()

class Goods(models.Model):
    items           = models.ForeignKey('Items.Items', db_index=True, on_delete=models.CASCADE)
    number          = models.IntegerField()
    price           = models.IntegerField()
    crawl_info      = models.ForeignKey(Crawl_Info, db_index=True, on_delete=models.CASCADE)
    uid             = models.CharField(max_length=20)
    def Option(self):
        return self.goods_option_set.all()


class Goods_Option(models.Model):
    goods           = models.ForeignKey(Goods,db_index=True,  on_delete=models.CASCADE)
    optionType      = models.TextField()
    optionValue     = models.IntegerField()

class Crawl_Summary(models.Model):
    date            = models.DateField(auto_now_add = True, db_index=True)
    serverid        = models.IntegerField(db_index= True)
    updated         = models.DateTimeField(auto_now=True)
    def Goods(self):
        return self.goods_summary_set.all()

class Goods_Summary(models.Model):
    items           = models.ForeignKey('Items.Items', db_index=True, on_delete=models.CASCADE)
    number          = models.IntegerField()
    price           = models.IntegerField()
    high            = models.IntegerField()
    low             = models.IntegerField()
    crawl_summary   = models.ForeignKey(Crawl_Summary, db_index=True, on_delete=models.CASCADE)
    def Option(self):
        return self.goods_option_set.all()

    