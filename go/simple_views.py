from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.http import HttpResponseRedirect
from go.models import CsgoApi
from django.db.models import Q
# from django.core.mail import send_mail

from go import golablib
from urllib import parse

# Create your views here.

# ajax:load exinfo
# monitor using server/administration page:monitoring+declare-info+shringking-database
# phone-verification-code/payment


def home(request):
    return render(request,'home.html')
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
    fade = ["刺刀","M9刺刀","爪子刀","穿肠刀"",猎杀者匕首","折叠刀","弯刀","鲍伊猎刀","蝴蝶刀","暗影双匕"]
    marble = ["刺刀","折叠刀","爪子刀","穿肠刀"]
    keyword = request.GET.get('keywords',None)
    index = ""
    item_info = {}
    if keyword != None and keyword != '':
        search_result = CsgoApi.objects.filter(Q(buff_name__contains=keyword)|Q(igxe_name__contains=keyword))
        index = "search result"
        if len(search_result) != 0:
            for i,item in enumerate(search_result):
                if item.catagory in fade and "渐变之色" in item.buff_name:
                    ex_info = "1"
                elif item.catagory in marble and "渐变大理石" in item.buff_name:
                    ex_info = "3"
                elif item.catagory == "AK-47" and "表面淬火" in item.buff_name:
                    ex_info = "2"
                else:
                    ex_info = "0"
                href = "./"+"item/"+str(item.buff_api)+"--"+item.igxe_api+ "--"+str(item.buff_name)+"--"+ex_info +"--"+"1"+"/"
                href = parse.quote(href)
                item_temp_info = {
                    "name":item.buff_name,
                    "catagory":item.catagory,
                    "rarity":item.rarity,
                    "icon":item.icon_url,
                    "href":href,
                }
                item_temp_list = [item_temp_info]
                if i == 0:
                    item_info[item.catagory] = item_temp_list
                elif i>0 and item_info.get(item.catagory) is None:
                    item_info[item.catagory] = item_temp_list
                else:
                    item_info[item.catagory].append(item_temp_info)
    context = {
        'search_item' : keyword,
        'search_result':item_info,
        "index":index,
        }
    return render(request,'search_result.html',context)
def show_item(request,api):
    brief_sell_status = []
    igxe_api = api.split('--')[1]
    buff_api = api.split('--')[0]
    item_name = api.split('--')[2]
    ex_info = api.split('--')[3]
    page_num = api.split('--')[4]
    try:
        page_num = int(page_num)
    except:
        page_num = 1
    buff_sell_num,buff_item = golablib.get_buff_detail(buff_api,page_num)
    if igxe_api != '':
        ig_sell_num,ig_item = golablib.get_igxe_detail(igxe_api,page_num)
        ig_min_price = ig_item[0]["price"]
    else:
        ig_sell_num = "null"
        ig_min_price = "null"
        ig_item = []
    buff_min_price = buff_item[0]["price"]
    brief_sell_status = [ig_sell_num,buff_sell_num,ig_min_price,buff_min_price,page_num]
    ranked_item = golablib.rank_items(ig_item+buff_item)
    igxe_link = "https://www.igxe.cn/product/{}".format(igxe_api)
    buff_link = "https://buff.163.com/market/goods?goods_id={}&from=market#tab=selling".format(buff_api)
    context = {
        'ex_info':ex_info,
        'items':ranked_item,
        "igxe_link":igxe_link,
        "buff_link":buff_link,
        "sell_status":brief_sell_status,
        "name":item_name
        }
    return render(request,'show_item.html',context)

# def faq(request):
#     return render(request,'faq.html')
# def contact_us(request):
#     return render(request,'contact_us.html')

import requests
from bs4 import BeautifulSoup
def check_igxe(name):
    check_url = "https://www.igxe.cn/csgo/730?keyword={}".format(name)
    check_page = requests.get(check_url)
    soup = BeautifulSoup(check_page.text,'html.parser')
    check_data = soup.find('div',attrs={'class':'dataList'})
    if check_data.find('a'):
        check_api = check_data.find('a')['href'].strip("/product")
        return check_api
    else:
        return ''
def buff_search(catagory,page="1"):
    eng_list = ["Glock-18","Five-Seven","Desert-Eagle","Dual Berettas","Nova","Sawed-Off","Negev","FAMAS","Galil AR","M4A1 消音版"]
    chi_list = ["格洛克 18 型","FN57","沙漠之鹰","双持贝瑞塔","新星","截短霰弹枪","内格夫","法玛斯","加利尔 AR","M4A1 消音型"]
    search_url = "https://buff.163.com/api/market/goods?game=csgo&page_num={}&category_group={}&page_size=50".format(page,catagory)
    r = requests.get(search_url)
    if r.status_code == 200:
        data = r.json()
        total_page = data["data"]["total_page"]
        all_item = data["data"]["items"]
        for single_item in all_item:
            buff_api = single_item["id"]
            buff_name = single_item["name"]
            if catagory == "hands":
                weapon = single_item["goods_info"]["info"]["tags"]["type"]["localized_name"]
            else:
                weapon = single_item["goods_info"]["info"]["tags"]["weapon"]["localized_name"]
            rarity = single_item["goods_info"]["info"]["tags"]["rarity"]["localized_name"]
            icon_url = single_item["goods_info"]["icon_url"]
            try:
                skin = CsgoApi.objects.get(buff_api=buff_api)
            except CsgoApi.DoesNotExist:
                add_skin = CsgoApi(buff_api=buff_api,buff_name=buff_name,catagory=weapon,rarity=rarity,icon_url=icon_url)
                add_skin.save()
                igxe_api = check_igxe(buff_name)
                igxe_name = buff_name
                if igxe_api == '':
                    chi_name = buff_name.split('|')[0].split('(')[0].strip(' ')
                    if chi_name in chi_list:
                        i = chi_list.index(chi_name)
                        re_name = buff_name.replace(chi_name,eng_list[i])
                        igxe_api = check_igxe(re_name)
                        igxe_name = re_name
                    else:
                        pass
                else:
                    pass
                add_skin.igxe_api = igxe_api
                add_skin.igxe_name = igxe_name
                add_skin.save()
                if igxe_api == '':
                    print(buff_name)
                    # f.write("{}\n".format(buff_name))
                else:
                    pass
            else:
                skin.buff_name = buff_name
                skin.rarity = rarity
                skin.icon_url = icon_url
                skin.igxe_name = buff_name
                skin.catagory = weapon
                skin.save()
                if skin.igxe_api == '':
                    igxe_api = check_igxe(buff_name)
                    igxe_name = buff_name
                    if igxe_api == '':
                        chi_name = buff_name.split('|')[0].split('（')[0].strip(' ')
                        if chi_name in chi_list:
                            i = chi_list.index(chi_name)
                            re_name = buff_name.replace(chi_name,eng_list[i])
                            igxe_api = check_igxe(re_name)
                            igxe_name = re_name
                        else:
                            pass
                    else:
                        pass
                    skin.igxe_api = igxe_api
                    skin.igxe_name = igxe_name
                    skin.save()
                    if igxe_api == '':
                        # f.write("{}\n".format(buff_name))
                        print(buff_name)
                    else:
                        pass
        print("page {} saved,of {} pages in {} catagory".format(page,total_page,catagory))
        return
def shrinking_database(request):
    catagory_list = ["knife","pistol","rifle","smg","shotgun","machinegun","hands"]
    # f = open('missed.txt','w')
    for i,cata in enumerate(catagory_list):
        if i>5:
            search_url = "https://buff.163.com/api/market/goods?game=csgo&page_num=1&category_group={}&page_size=50".format(cata)
            r = requests.get(search_url)
            data = r.json()
            total_page = data["data"]["total_page"]
            for page in range(total_page):
                page_now = str(page + 1)
                buff_search(cata,page_now)
        print("{} checked".format(cata))
    # f.close()
    return render(request,'sign_in.html')