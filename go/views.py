from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from go.models import User,CsgoApi
from django.core.mail import send_mail

from golab import gen_vercode
import os

# Create your views here.
# protection:user/payment/level/change-psss/


def user(request):
    context = {}
    vip_info = []
    monitor_space = 2
    isvip = False
    try:
        user = User.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect('/gogate/sign-in/')
    if request.session.get('authenticated',False):
        if user.is_vip == True:
            isvip = True
            current_monitor_num = len(user.monitored_buff_apis.strip('*').split('**'))
            if request.GET.get('buff_api','') != '':
                if user.number_of_items>current_monitor_num:
                    monitor_space = 1
                    buff_api = request.GET.get('buff_api')
                    ig_api = request.GET.get('ig_api')
                    max_price = request.GET.get('max_price')
                    max_wear = request.GET.get('max_wear')
                    rare_info = request.GET.get('rare')
                    user.monitored_buff_apis = user.monitored_buff_apis + "**" + buff_api
                    user.monitored_igxe_apis = user.monitored_igxe_apis + "**" + ig_api
                    user.price_restrictions = user.price_restrictions + "**" + max_price
                    user.wear_restrictions = user.wear_restrictions + "**" + max_wear
                    user.rare_restrictions = user.rare_restrictions + "**" + rare_info
                    user.save()
                else:
                    monitor_space = 0
        if user.monitored_buff_apis != '':
            monitored_buff_apis = user.monitored_buff_apis
            monitored_igxe_apis = user.monitored_igxe_apis
            price = user.price_restrictions
            wear = user.wear_restrictions
            rare = user.rare_restrictions
            buff_api_list = monitored_buff_apis.strip('*').split('**')
            if buff_api_list != ['']:
                igxe_api_list = monitored_igxe_apis.strip('*').split('**')
                price_list = price.strip('*').split('**')
                wear_list = wear.strip('*').split('**')
                rare_list = rare.strip('*').split('**')
                for i,item_api in enumerate(buff_api_list):
                    usr_item = CsgoApi.objects.get(buff_api=item_api)
                    remove_href = "/gogate/remove_item?buff={}&igxe={}&price={}&wear={}&rare={}".format(item_api,igxe_api_list[i],price_list[i],wear_list[i],rare_list[i])
                    temp_vip_info = {
                        "item_name":usr_item.buff_name,
                        "price":price_list[i],
                        "wear":wear_list[i],
                        "rare":rare_list[i],
                        "remove_href":remove_href
                    }
                    vip_info.append(temp_vip_info)
        context = {
            'monitor_space':monitor_space,
            'usr_info':vip_info,
            'isvip':isvip,
        }
        return render(request,'user.html',context)
    else:
        return HttpResponseRedirect('/gogate/sign-in/')
def choose_level(request):
    try:
        user = User.objects.get(username=request.session['username'])
    except:
        return HttpResponseRedirect('/gogate/sign-in/')
    if user.monitored_buff_apis == '':
        context = {
            # 'send_to_email':False,
            'number_of_items':0,
            'check_freq':0,
            'start_day':0,
            'time_span':0
        }
    else:
        context = {
            # 'send_to_email':user.send_to_mail,
            'number_of_items':user.number_of_items,
            'check_freq':user.check_frequency,
            'start_day':user.start_day,
            'time_span':user.time_span
        }
    return render(request,'choose_level.html',context)

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
                request.session['isvip'] = user.is_vip
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
    return render(request,'login_register.html',{'auth':authentication,'img':img_src,"index":"in"})
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
                request.session['isvip'] = False
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
    return render(request,'login_register.html',{'img':img_src,"index":"up"})
def sign_out(request):
    request.session['authenticated'] = False
    return HttpResponseRedirect('/gogate/')
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
    total_pay = 0
    # if request.is_ajax():
    #     if request.POST.get('paymsg') == 1:
    if request.method == "POST":
        num_index = ["1","3","5"]
        freq_index = ["2","5","9"]
        span_index = ["2","5","9"]
        number_of_items = request.POST.get("number_of_items")
        check_freq = request.POST.get("check_freq")
        time_span = request.POST.get("time_span")
        total_pay = 3 + num_index.index(number_of_items) + freq_index.index(check_freq) + span_index.index(time_span)
    return render(request,'payment.html',{"payamount":total_pay,})
def forget_pass(request):
    return render(request,'forget_pass.html')