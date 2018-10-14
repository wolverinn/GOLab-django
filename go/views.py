from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from go.models import User
from django.core.mail import send_mail

from go import gen_vercode
import os

# after online:phone-verification-code/payment

# html-base-head&foot(log-state)
# js funcs:login-before-monitor
# 玄学，Ajax加载搜索结果，igxe-api


# Create your views here.


def jsapi(request):
    return render

def user(request):
    context = {}
    user = User.objects.get(username=request.session['username'])
    if request.session.get('authenticated',False):
        if user.is_vip == True:
            if request.GET.get('item_name',None) != None:
                item_name = request.GET.get('item_name')
                max_price = request.GET.get('max_price')
                max_wear = request.GET.get('max_wear')
                user.monitored_items = user.monitored_items + "**" + item_name
                user.maximum_price = user.maximum_price + "**" + max_price
                user.maximum_wear = user.maximum_wear + "**" + max_wear
                user.save()
        if user.monitored_items != '':
            monitored_items = user.monitored_items
            price = user.price_restrictions
            wear = user.wear_restrictions
            rare = user.rare_restrictions
            item_list = monitored_items.split('**')
            price_list = price.split('**')
            wear_list = wear.split('**')
            rare_list = rare.split('**')
            len_item_list = list(range(len(item_list)))
            context = {
                'monitored_items':item_list,
                'price':price_list,
                'wear':wear_list,
                'rare':rare_list,
                'isvip':True,
                'len_list':len_item_list
            }
        else:
            context = {
                'monitored_items':'',
                'price':'',
                'wear':'',
                'rare':'',
                'isvip':False,
                'len_list':[]
            }
        return render(request,'user.html',context)
    else:
        return HttpResponseRedirect('/gogate/sign-in/')
def sign_in(request):
    try:
        os.remove('./static/img/{}.png'.format(request.session['photo_vercode']))
    except:
        pass
    username = request.POST.get('username',None)
    password = request.POST.get('password',None)
    vercode = request.POST.get('vercode',None)
    if username != None and password != None and vercode != None:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            correct_vercode = gen_vercode.gene_code(4)
            request.session['photo_vercode'] = correct_vercode
            img_src = "./img/{}.png".format(correct_vercode)
        else:
            if password == user.password and vercode == request.session['photo_vercode']:
                request.session['authenticated'] = True
                request.session['username'] = username
            else:
                correct_vercode = gen_vercode.gene_code(4)
                request.session['photo_vercode'] = correct_vercode
                img_src = "./img/{}.png".format(correct_vercode)
                request.session['authenticated'] = False
    else:
        correct_vercode = gen_vercode.gene_code(4)
        request.session['photo_vercode'] = correct_vercode
        img_src = "./img/{}.png".format(correct_vercode)
    authentication = request.session.get('authenticated',False)
    if authentication is True:
        return HttpResponseRedirect('/gogate/user/')
    return render(request,'sign_in.html',{'auth':authentication,'img':img_src})
def sign_up(request):
    try:
        os.remove('./static/img/{}.png'.format(request.session['photo_vercode']))
    except:
        pass
    username = request.POST.get('username',None)
    password = request.POST.get('password',None)
    vercode = request.POST.get('vercode',None)
    if username != None and password != None and vercode != None:
        if vercode == request.session.get('photo_vercode',False):
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username,password=password)
                user.save()
                request.session['authenticated'] = True
                request.session['username'] = username
            else:
                correct_vercode = gen_vercode.gene_code(4)
                request.session['photo_vercode'] = correct_vercode
                img_src = "./img/{}.png".format(correct_vercode)
        else:
            correct_vercode = gen_vercode.gene_code(4)
            request.session['photo_vercode'] = correct_vercode
            img_src = "./img/{}.png".format(correct_vercode)
    else:
        correct_vercode = gen_vercode.gene_code(4)
        request.session['photo_vercode'] = correct_vercode
        img_src = "./img/{}.png".format(correct_vercode)
    authentication = request.session.get('authenticated',False)
    if authentication is True:
        return HttpResponseRedirect('/gogate/user/')
    return render(request,'sign_up.html',{'auth':authentication,'img':img_src})
def sign_out(request):
    request.session['authenticated'] = False
    return render(request,'base.html',{'index':'','search_result':None,'auth':False})
def change_password(request):
    msg = ""
    old_pass = request.POST.get("old_pass")
    new_pass1 = request.POST.get("new_pass")
    user = User.objects.get(username=request.session['username'])
    if old_pass == user.password:
        user.password = new_pass1
        user.save()
        msg = "ok"
    else:
        msg = "old password incorrect"
    return render(request,'change_pass.html',{'msg':msg})
def choose_level(request):
    user = User.objects.get(username=request.session['username'])
    if user.monitored_items == '':
        context = {
            'send_to_email':False,
            'number_of_items':0,
            'check_freq':0,
            'start_day':0,
            'time_span':0
        }
    else:
        context = {
            'send_to_email':user.send_to_email,
            'number_of_items':user.number_of_items,
            'check_freq':user.check_frequency,
            'start_day':user.start_day,
            'time_span':user.time_span
        }
    return render(request,'choose_level.html',context)
def change_email(request):
    if request.session.get('authenticated',False):
        msg = "mail"
        newmail = request.POST.get('newmail',None)
        vercode_get = request.POST.get('vercode',None)
        if newmail != None and vercode_get == None:
            msg = "vercode"
            vercode = gen_vercode.gen_text(6)
            request.session['email_vercode'] = vercode
            content = "your verification code:"+vercode
            send_mail(
                'golab|change email',
                content,
                'emzdn@163.com',
                [str(newmail)],
                fail_silently=False,
            )
        elif vercode_get != None:
            if vercode_get == request.session['email_vercode']:
                user = User.objects.get(username=request.session['username'])
                user.email = newmail
                user.save()
                msg = "complete"
        else:
            pass
        return render(request,'change_email.html',{'msg':msg,'newmail':newmail})
    else:
        return HttpResponseRedirect('/gogate/sign-in/')

def payment(request):
    return render(request,'payment.html')
def new_item(request):
    item_name = request.GET.get('name')
    return render(request,'new_item.html',{'item_name':item_name})
def forget_pass(request):
    return render(request,'forget_pass.html')