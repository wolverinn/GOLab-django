import requests
import random

from go.models import CsgoApi


def get_igxe_detail(igxe_api,page_num):
    igxe_item = []
    for page_no in range(page_num):
        page_no = page_no + 1
        api_url = "https://www.igxe.cn/product/trade/" + igxe_api + "?page_no={}".format(str(page_no))
        api_request = requests.get(api_url)
        if api_request.status_code is 200:
            data = api_request.json()
            page_count = data["page"]["page_count"]
            item_count = data["page"]["total"]
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
            if page_no == page_count:
                break
        else:
            print("igxe api failed")
    return item_count,igxe_item

def get_buff_detail(buff_api,page_num):
    buff_item = []
    page_num = page_num*10
    api_url = "https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={}&page_num=1&page_size={}".format(buff_api,page_num)
    api_request = requests.get(api_url)
    if api_request.status_code is 200:
        data = api_request.json()
        # page_count = data["data"]["total_page"]
        item_count = data["data"]["total_count"]
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
    else:
        print("buff api failed")
    return item_count,buff_item

def rank_items(all_items): 
    ranked_list = sorted(all_items, key=lambda item: float(item["price"]))
    return ranked_list
def gen_vercode(num):
    vercode = ""
    number = list(range(10))
    ver_list = random.sample(number,num)
    for i in ver_list:
        vercode = vercode + str(i)
    return vercode


def monitor(igxe_api,buff_api,price,wear):
    igxe_url = "https://www.igxe.cn/product/trade/" + igxe_api + "?page_no=1"
    buff_url = "https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={}&page_num=1&page_size=50".format(buff_api)
    igxe_r = requests.get(igxe_url)
    igxe_json = igxe_r.json()
    for item in igxe_json["d_list"]:
        if item["unit_price"] <= price:
            if item["exterior_wear"] <= wear:
                return 1
            else:
                continue
        else:
            break
    buff_r = requests.get(buff_url)
    buff_json = buff_r.json()
    for item in buff_json["data"]["items"]:
        if item["price"] <= price:
            if item["asset_info"]["paintwear"] <= wear:
                return 1
            else:
                continue
        else:
            break
    return 0
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