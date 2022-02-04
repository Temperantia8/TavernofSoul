from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Market.models import Crawl_Info, Goods, Goods_Option
from Items.models import Items, Equipments
from rest_framework.decorators import api_view
import logging
import datetime
from itertools import islice
from ipfparser.utils import *
from django.shortcuts import render
from django.conf import settings
from os.path import join
from django.http import HttpResponse

APP_NAME = 'Market'

server_list={
    'itos':{
        '1004' : 'Telsiai' ,
    }

}
allowed = ['itos', 'test']

def bulk_op(operation, objs, batch_size, fields = False):
    count = 0
    leng = len(objs)
    batch_size = int(batch_size)
    ret = []
    while True:
        # logging.warning("---- bulk %s %s / %s | %s" %('update' if fields else 'insert',  batch_size * count, leng, count))
        batch = list(islice(objs,count* batch_size, (count+1) * batch_size))
        if not batch:
            break
        if fields:
            ret+=operation(batch, fields, batch_size)    
        else:
            ret+=operation(batch, batch_size)
        count+=1
    return ret

@api_view(['POST'])
def post(request):
    market = request.data
    # try:
    try:
        Crawl_Info.objects.get(market['crawlUuid'])
        return Response({"status": "success", "data": ''}, status=status.HTTP_200_OK)
    except:
        pass
    handler = Crawl_Info(crawl_uuid = market['crawlUuid'], serverid = market['serverId'])
    items = {i.id_name :i for i in Items.objects.all()}
    handler.save()
    batch = []
    for key in market['storedItemInfo']:
        item = market['storedItemInfo'][key]
        try:
            # item_handler = Items.objects.get(id_name=item['className'])
            item_handler = items[item['className']]
        except:
            logging.warning('item not found')
            continue 
        goods_handler = Goods(items = item_handler, number = item['number'], price=item['price'], crawl_info = handler, uid = key)
        # goods_handler.save()
        batch.append(goods_handler)

    goods_list =  bulk_op(Goods.objects.bulk_create, batch, 100)
    goods = {i.uid : i for i in Goods.objects.filter(crawl_info = handler)}
    # goods = {}
    # for i in range(len(batch)):
        # goods[batch[i].uid] = goods_list[i].id

    
    batch = []
    for key in market['storedItemInfo']:
        item = market['storedItemInfo'][key]
        for i in item['randomOption'] + item['hatOption']:
            if i['has']:
                opt = Goods_Option(optionValue = i['optionValue'], optionType = i['optionType'], goods = goods[key])
                batch.append(opt)  
    bulk_op(Goods_Option.objects.bulk_create, batch, 100)        

    return Response({"status": "success", "data": ''}, status=status.HTTP_200_OK)
    # except:
        # return Response({"status": "error", "data": ''}, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        return Response({"status": "error", "data": ''}, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    if settings.REGION not in allowed:
        return HttpResponse('m(._.)m')
    data                = {}
    data['query']       = getFromGet(request, 'q','')
    data['curpage']     = int(getFromGet(request, 'page',1))

    type_n              = getFromGet(request, 'type', '')
    data['types']       = []
    for i in Items.objects.values('type').distinct() :
        if i['type'] != '':
            data['types'].append({'type':i['type'].lower(), 'id' : i['type']})
    for i in Equipments.objects.values('type_equipment').distinct() :
        if i['type_equipment'] != '':
                data['types'].append({'type':(i['type_equipment'].lower()), 'id' : '%s_eq'%(i['type_equipment'])})

    try:
        data['server_list'] = server_list[settings.REGION]
    except:
        data['server_list'] = server_list['itos']

    server = getFromGet(request,'server', list( data['server_list'].keys())[0])
    data['crawl']       = Crawl_Info.objects.filter(serverid = server).latest('created')

    order               = getFromGet(request,'order','price-asc')
    data['order']       = order 
    order               = order.split("-")
    srt                 = '' if order[-1] == 'asc' else '-'
    order               = srt+order[0]


    data['item']        = data['crawl'].Goods().filter(items__name__icontains= data['query']).order_by(order)

    if (type_n != ''):
        if ('_eq' in type_n):
            type_n = type_n.replace("_eq", '')
            data['item'] = data['item'].filter(items__equipments__type_equipment =type_n)
        else:
            data['item'] = data['item'].filter(items__type =type_n)

    data['type']        = getFromGet(request, 'type', '')
    data['item_len']    = len(data['item'])
    data['item']        = data['item'][(data['curpage']-1)*20:data['curpage']*20]

    
    

    pages = list(range(math.ceil(data['item_len']/20) +1))
    pages.remove(0) #there's no page 0
    makePagination(request, data, pages, 11 )

    return render(request, join(APP_NAME,"index.html"), data)

