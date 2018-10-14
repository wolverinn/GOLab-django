from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
# from go.models import User
# from django.core.mail import send_mail

from go import golablib

# Create your views here.

def home(request):
    response = HttpResponse()
    response.write("<h1>welcome,begin <a href = './gogate'>searching</a></h1>")
    return response
def head(request):
    return render(request,'head.html')
def foot(request):
    return render(request,'foot.html')
def user_state(request):
    auth = request.session.get('authenticated',False)
    isvip = request.session.get('isvip',False)
    if auth == False:
        return JsonResponse({'state':0})
    elif isvip == False:
        return JsonResponse({'state':1})
    else:
        return JsonResponse({'state':2})

def search(request):
    if request.is_ajax():
        keyword = request.GET.get('keywords',None)
        page = request.GET.get('page_num',"1")
        search_result,total_page = golablib.search_item(keyword,page)
        index = "search result"
        return JsonResponse({'search_result':search_result})
    authentication = request.session.get('authenticated',False)
    keyword = request.GET.get('keywords',None)
    page = request.GET.get('page_num',"1")
    if keyword != None:
        search_result,total_page = golablib.search_item(keyword,page)
        index = "search result"
    else:
        search_result = None
        total_page = 0
        index = ""
    context = {
        'search_result':search_result,
        'search_item':keyword,
        "index":index,
        'auth':authentication,
        'total':total_page,
        "current":page
        }
    return render(request,'base.html',context)
def show_item(request,api):
    igxe_api = api.split('--')[1]
    buff_api = api.split('--')[0]
    item_name = api.split('--')[2]
    ig_item = golablib.get_igxe_detail(igxe_api)
    buff_item = golablib.get_buff_detail(buff_api)
    ranked_item = golablib.rank_items(ig_item+buff_item)
    igxe_link = "https://www.igxe.cn/product/{}".format(igxe_api)
    buff_link = "https://buff.163.com/market/goods?goods_id={}&from=market#tab=selling".format(buff_api)
    context = {
        'items':ranked_item,
        "igxe_link":igxe_link,
        "buff_link":buff_link,
        "name":item_name
        }
    return render(request,'show_item.html',context)

# def faq(request):
#     return render(request,'faq.html')
# def contact_us(request):
#     return render(request,'contact_us.html')