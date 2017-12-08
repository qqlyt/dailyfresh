# coding=utf8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect
import user_decorator
from df_goods.models import GoodsInfo



def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    # 接受输入
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2=post.get('cpwd')
    uemail=post.get('email')

    # 判断密码是否一致
    if upwd!=upwd2:
        return redirect('/user/register/')

    # 用sha1加密密码
    s1=sha1()
    s1.update(upwd)
    upwd3=s1.hexdigest()

    # 存储数据
    user=UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()

    return redirect('/user/login/')

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.object.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname','')
    context ={'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    remember = post.get('remember',0)
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)

    if len(users)==1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            url = request.COOKIES.get('url','/')
            red = HttpResponseRedirect(url)
            if remember!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_uname']=uname
            return red
        else:
            context = {'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html',context)

    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

@user_decorator.login
def info(request):


    user = UserInfo.objects.get(id = request.session['user_id'])
    uemail = user.uemail

    goods_ids = request.COOKIES.get('goods_ids','')
    goods_list = []
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(pk=int(goods_id)))

    context = {'page_name':1,'title':'用户中心',
               'uname':request.session['user_uname'],
               'uemail':uemail,
               'goods_list':goods_list}
    return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def order(request):
    context={'page_name':1,'title':'用户中心'}
    return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post = request.POST
        user.uaddress = post.get('uaddress')
        user.uaddressee = post.get("uaddressee")
        user.upostal_code = post.get('upostal_code')
        user.uphone = post.get('uphone')
        user.save()
    context={'page_name':1,'title':'用户中心','uaddress':user.uaddress,"uaddressee":user.uaddressee,'upostal_code':user.upostal_code,'uphone':user.uphone}
    return render(request,'df_user/user_center_site.html',context)






