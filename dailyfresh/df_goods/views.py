# coding=utf8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
from df_cart.models import CartInfo

def index(request):
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    cart_count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
    context={'title':'首页','guest_cart':1,
             'cart_count':cart_count,
             'type0':type0,'type01':type01,
             'type1': type1, 'type11': type11,
             'type2': type2, 'type21': type21,
             'type3': type3, 'type31': type31,
             'type4': type4, 'type41': type41,
             'type5': type5, 'type51': type51,
             }
    return render(request,'df_goods/index.html',context)

def list(request,title_id,page_id,sort_id):
    typeinfo = TypeInfo.objects.get(pk=int(title_id))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort_id== '1':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(title_id)).order_by('-id')
    if sort_id== '2':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(title_id)).order_by('gprice')
    if sort_id== '3':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(title_id)).order_by('-gclick')
        
    paginator = Paginator(goods_list,1)
    page = paginator.page(int(page_id))
    cart_count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
    context = {'title':typeinfo.ttitle,'guest_cart':1,
               'cart_count': cart_count,
               'paginator':paginator,
               'page':page,
               'news':news,
               'sort_id':sort_id,
               'typeinfo':typeinfo}
    return render(request,'df_goods/list.html',context)

def detail(request,id):
    goods = GoodsInfo.objects.get(pk=int(id))
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    goods.gclick += 1
    goods.save()
    cart_count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
    context = {'title':goods.gtitle,'guest_cart':1,
               'goods':goods,'news':news,
               'cart_count':cart_count
               }
    response = render(request, 'df_goods/detail.html', context)

    # 记录最近浏览，在用户中心使用
    goods_ids = request.COOKIES.get('goods_ids','')
    goods_id = '%d' %goods.id
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        if goods_ids1.count(goods_id)>=1:
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0,goods_id)
        if len(goods_ids1) >= 6:
            goods_ids1.pop()
        goods_ids= ','.join(goods_ids1)
    else:
        goods_ids = goods_id
    response.set_cookie('goods_ids',goods_ids)

    return response




