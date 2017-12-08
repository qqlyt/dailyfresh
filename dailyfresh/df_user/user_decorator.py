from django.shortcuts import redirect
from django.http import HttpResponseRedirect

def login(fun):
    def login_fun(request,*args,**kwargs):
        if request.session.has_key('user_id'):
            return fun(request,*args,**kwargs)
        else:
            red = HttpResponseRedirect('/user/login')
            red.set_cookie('url',request.get_full_path())
            return red
    return login_fun
