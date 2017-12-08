# coding=utf8
from django.shortcuts import render,redirect
from models import *
from django.http import JsonResponse
from df_user import user_decorator



@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {'page_name':1,'title':'购物车','carts':carts,}
    return render(request,'df_cart/cart.html',context)


@user_decorator.login
def add(request,gid,count):
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)

    carts = CartInfo.objects.filter(goods_id=gid,user_id=uid)
    if len(carts)>=1:
        cart = carts[0]
        cart.count += count
    else:
        cart = CartInfo()
        cart.goods_id = gid
        cart.user_id = uid
        cart.count = count
    cart.save()

    if request.is_ajax():

        count = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'count':count})
    else:
        return redirect('/cart')

@user_decorator.login
def edit(request,cart_id,count):
    try:
        cart = CartInfo.objects.get(id=cart_id)
        count1 = cart.count
        cart.count = int(count)
        cart.save()
        data = {'ok':0}
    except Exception:
        data = {'ok': count1}
    return JsonResponse(data)

@user_decorator.login
def delete(request,cart_id):
    try:
        cart = CartInfo.objects.get(pk=cart_id)
        cart.delete()
        data = {'ok':1}
    except Exception:
        data = {'ok':0}
    return JsonResponse(data)