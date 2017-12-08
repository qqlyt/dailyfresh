#coding=utf8
from django.shortcuts import render,redirect
from df_user.models import UserInfo
from df_user import user_decorator
from df_cart.models import *
from df_goods.models import *
from django.db import transaction
from models import *
from datetime import datetime
from decimal import *

@user_decorator.login
def order(request):
    user = UserInfo.objects.get(pk=request.session['user_id'])
    get = request.GET
    cart_ids = get.getlist('cart_id')
    cart_ids1 = [int(item) for item in cart_ids ]
    carts = CartInfo.objects.filter(pk__in = cart_ids1)
    context ={'title':'提交订单',
              'page_name':1,
              'carts':carts,
              'cart_ids':','.join(cart_ids),
              'user':user }
    return render(request,'df_order/order.html',context)

@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()

    cart_ids = request.POST.get('cart_ids')
    try:
        # 创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d' %(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(request.POST.get('total'))
        order.save()
        # 创建详单对象
        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids1:
            detail = OrderDetailInfo()
            detail.order = order
            # 查询购物车信息
            cart = CartInfo.objects.get(pk=id1)
            # 判断商品库存
            goods = cart.goods
            if goods.gstock > cart.count:
                goods.gstock -= cart.count
                goods.save()
                # 完善订单信息
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                # 删除购物车数据
                cart.delete()
            else:#如果库存量小于购买量
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print '================%s' %e
        transaction.savepoint_rollback(tran_id)

    return redirect('/user/order')
