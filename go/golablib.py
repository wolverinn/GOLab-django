import requests
from bs4 import BeautifulSoup
from urllib import parse
import random

from go.models import CsgoApi

def search_item(keyword):
    item = []
    def check_igxe(name):
        check_url = "https://www.igxe.cn/csgo/730?keyword={}".format(name)
        check_page = requests.get(check_url)
        soup = BeautifulSoup(check_page.text,'html.parser')
        check_data = soup.find('div',attrs={'class':'dataList'})
        if check_data.find('a'):
            check_api = check_data.find('a')['href'].strip("/product")
            check_price = check_data.find('span').string + check_data.find('sub').string
            check_num = check_data.find('div',attrs={'class','sum fr'}).string
            return check_api,check_num,check_price
        else:
            return '','',''
    def buff_search(keyword,page_num="1"):
        search_api = "https://buff.163.com/api/market/goods?game=csgo&page_num={}&search={}".format(page_num,keyword)
        search_action = requests.get(search_api)
        if search_action.status_code is 200:
            search_result = search_action.json()
            total_page = search_result["data"]["total_page"]
            if total_page == 0:
                return item
            all_item = search_result["data"]["items"]
            for single_item in all_item:
                if single_item["goods_info"]["info"]["tags"].get("exterior") is None:
                    wear_catagory = None
                else:
                    wear_catagory = single_item["goods_info"]["info"]["tags"]["exterior"]["localized_name"]
                buff_api = single_item["id"]
                name = single_item["name"]
                ig_sell_num = ''
                ig_min_price = ''
                try:
                    skin = CsgoApi.objects.get(buff_api=buff_api)
                except CsgoApi.DoesNotExist:
                    igxe_api = ''
                else:
                    igxe_api = skin.igxe_api
                if igxe_api != '':
                    igxe_url = "https://www.igxe.cn/product/trade/" + igxe_api
                    igxe_request = requests.get(igxe_url)
                    if igxe_request.status_code is 200:
                        data = igxe_request.json()
                        ig_sell_num = data["page"]["total"]
                        ig_min_price = data["d_list"][0]["unit_price"]
                else:
                    igxe_api,ig_sell_num,ig_min_price = check_igxe(name)
                href = "./"+"item/"+str(buff_api)+"--"+igxe_api+ "--"+str(name) +"/"
                href = parse.quote(href)
                temp_info = {
                    "name": name,
                    "wear_catagory": wear_catagory,
                    "rarity": single_item["goods_info"]["info"]["tags"]["rarity"]["localized_name"],
                    "buff_api": buff_api,
                    "icon_url": single_item["goods_info"]["icon_url"],
                    "buff_sell_num": single_item["sell_num"],
                    "buff_min_price": single_item["sell_min_price"],
                    "igxe_api": igxe_api,
                    "ig_sell_num": ig_sell_num,
                    "ig_min_price": ig_min_price,
                    "href":href
                }
                item.append(temp_info)
            if total_page > int(page_num):
                page_num = str(int(page_num) + 1)
                buff_search(keyword,page_num)
    buff_search(keyword)
    return item
def get_igxe_detail(igxe_api,page_num="1"):
    igxe_item = []
    api_url = "https://www.igxe.cn/product/trade/" + igxe_api + "?page_no={}".format(page_num)
    api_request = requests.get(api_url)
    if api_request.status_code is 200:
        data = api_request.json()
        page_count = data["page"]["page_count"]
        item_list = data["d_list"]
        for item_detail in item_list:
            if item_detail.get("sticker") is None:
                temp_sticker = None
            else:
                temp_sticker = item_detail["sticker"]
            temp_detail = {
                "wear":item_detail["exterior_wear"],
                "steam_link":item_detail["actions_link"],
                "price":item_detail["unit_price"],
                "sticker":temp_sticker,
                "site":"igxe"
            }
            igxe_item.append(temp_detail)
        if int(page_num) < page_count:
            page_num = str(int(page_num)+1)
            get_igxe_detail(igxe_api,page_num)
    else:
        print("igxe api failed")
    return igxe_item

def get_buff_detail(buff_api,page_num="1"):
    buff_item = []
    api_url = "https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={}&page_num={}".format(buff_api,page_num)
    api_request = requests.get(api_url)
    if api_request.status_code is 200:
        data = api_request.json()
        page_count = data["data"]["total_page"]
        item_list = data["data"]["items"]
        for item_detail in item_list:
            temp_detail = {
                "wear": item_detail["asset_info"]["paintwear"],
                "steam_link": item_detail["asset_info"]["action_link"],
                "price": item_detail["price"],
                "sticker": item_detail["asset_info"]["info"]["stickers"],
                "site": "buff"
            }
            buff_item.append(temp_detail)
        if int(page_num) < page_count:
            page_num = str(int(page_num)+1)
            get_buff_detail(buff_api,page_num)
    else:
        print("buff api failed")
    return buff_item

def rank_items(all_items): 
    ranked_list = sorted(all_items, key=lambda item: item["price"])
    return ranked_list
def gen_vercode(num):
    vercode = ""
    number = list(range(10))
    ver_list = random.sample(number,num)
    for i in ver_list:
        vercode = vercode + str(i)
    return vercode

# additional，javascript
def csgola_info(inspect_link):
    import json
    data = {
        "inspecturl": inspect_link[66:]
    }
    header = {
        # "Accept": "*/*",
        # "Accept-Encoding": "gzip, deflate",
        # "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Length": "61",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "DNT": "1",
        "Host": "www.csgola.com",
        "Origin": "http://www.csgola.com",
        # "Proxy-Connection": "keep-alive",
        "Referer": "http://www.csgola.com/float/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    ses = requests.session()
    ses.get("http://www.csgola.com/float/")
    query_url = "http://www.csgola.com/market_item_detail"
    content = ses.post(query_url, data=data, headers=header)
    content_text=content.text
    text=content_text.replace('\ufeff','')
    item_data=json.loads(text)
    msg = ""
    if str(item_data["error"]) == "0":
        if item_data["msg"]["iffade"] is True:
            fadepercent = item_data["msg"]["fadepercent"]
            msg = "渐变百分比：{}".format(fadepercent)
        if item_data["msg"]["ifakcase"] is True:
            pattern = item_data["msg"]["akcase_i"]
            quality = item_data["msg"]["akcase_p"]
            msg = "pattern:{}-T{}".format(pattern,str(quality))
        if item_data["msg"]["ificefire"] is True:
            icefire = item_data["msg"]["icefirelv"]
            msg = "{}档冰火".format(str(icefire))
    else:
        print(item_data["error"])
    return msg