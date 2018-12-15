import requests
from go import golablib.monitor as monitor
import time
import datetime

# 不间断运行：https://blog.csdn.net/miner_zhu/article/details/81315974

api_v1 = 'http://47.107.40.103/gogate/api/v1/'

v1_data = {
    "key":"Wolverine",
    "freq":"2",
}
while True:
    v1_r = requests.get(api_v1,data=v1_data)
    v1_json = v1_r.json()
    all_f2 = v1_json["usr"]
    start = time.time()
    while True:
        for usr_f2 in all_f2:
            today = datetime.datetime.today()
            start_day = usr_f2["start_day"]
            # date = datetime.datetime.strptime(start_day,'%Y-%m-%d')
            if int((today-start_day).days) > usr_f2["span"]:
                cancle_vip_url = "http://47.107.40.103/gogate/api/v3/"
                v3_data = {
                    "key":"Wolverine",
                    "username":usr_f2["username"]
                }
                requests.get(cancle_vip_url,data=v3_data)
                continue
            buff_api_list = usr_f2["buff_apis"].strip("*").split("**")
            igxe_api_list = usr_f2["igxe_apis"].strip("*").split("**")
            price_list = usr_f2["price_restrictions"].strip("*").split("**")
            wear_list = usr_f2["wear_restrictions"].strip("*").split("**")
            rare_list = usr_f2["rare_restrictions"].strip("*").split("**")
            for i,single_buff_api in enumerate(buff_api_list):
                result = monitor(single_buff_api,igxe_api_list[i],price_list[i],wear_list[i])
                if result == 1:
                    username = usr_f2["username"]
                    remove_item_url = "http://47.107.40.103/gogate/api/v2/"
                    v2_data = {
                        "key":"Wolverine",
                        "username":username,
                        "buff_api":single_buff_api,
                        "igxe_api":igxe_api_list[i],
                        "price":price_list[i],
                        "wear":wear_list[i],
                        "rare":rare_list[i]
                    }
                    requests.get(remove_item_url,data=v2_data)
                    print("ok")
                else:
                    continue
        time.sleep(120)
        if time.time()-start > 5400:
            break