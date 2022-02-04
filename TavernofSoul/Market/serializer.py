from rest_framework import serializers
from .models import Crawl_Info, Goods, Goods_Option

# class CartItemSerializer(serializers.ModelSerializer):
#     product_name = serializers.CharField(max_length=200)
#     product_price = serializers.FloatField()
#     product_quantity = serializers.IntegerField(required=False, default=1)

#     class Meta:
#         model = CartItem
#         fields = ('__all__')

class Crawl_Info_Serializer(serializers.ModelSerializer):
    crawl_uuid      = serializers.CharField(max_length = 40)
    date            = serializers.DateTimeField(auto_now=True)
    class Meta:
        model = Crawl_Info
        fields = ('__all__')

class Goods_Serializer(serializers.ModelSerializer):
    items           = serializers.ForeignKey('Items.Items', db_index=True, on_delete=serializers.CASCADE)
    number          = serializers.IntegerField()
    price           = serializers.IntegerField()
    created         = serializers.DateTimeField(auto_now_add=True)
    updated         = serializers.DateTimeField(auto_now=True)
    serverid        = serializers.IntegerField(db_index=True)
    crawl_info      = serializers.ForeignKey(Crawl_Info, db_index=True, on_delete=serializers.CASCADE)
    class Meta:
        model = Goods
        fields = ('__all__')    

    
class Goods_Option_Serializer(serializers.ModelSerializer)::
    goods           = serializers.ForeignKey(Goods,db_index=True,  on_delete=serializers.CASCADE)
    optionType      = serializers.TextField()
    optionValue     = serializers.IntegerField()
    class Meta:
        model = Goods_Option
        fields = ('__all__')