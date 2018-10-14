from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# from go.models import User
# from django.core.mail import send_mail

from go import golablib

# Create your views here.

def home(request):
    response = HttpResponse()
    response.write("<h1>welcome,begin <a href = './gogate'>searching</a></h1>")
    return response

def search(request):
    authentication = request.session.get('authenticated',False)
    keyword = request.POST.get('keywords',None)
    if keyword != None:
        search_result = golablib.search_item(keyword)
        index = "search result"
    else:
        search_result = None
        index = ""
    return render(request,'base.html',{'search_result':search_result,"index":index,'auth':authentication})
def show_item(request,item,api):
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

def faq(request):
    return render(request,'faq.html')
def contact_us(request):
    return render(request,'contact_us.html')