# _*_coding:utf-8 _*_
# @Time    :2022/11/12 8:06
# @Author  :Godam
# @FileName:hsjg.py

# @Software:PyCharm

# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import time

# 以下内容无需改动
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"
host = "jksb.v.zzu.edu.cn"
origin = "https://jksb.v.zzu.edu.cn"
session = requests.session()
info = ["0", "1"]
result = []

data = {
    "ptopid": "",
    "sid": "",
}


# 读取账号密码信息
def read_users(path):
    data_frame = pd.read_excel(path)
    df_li = data_frame.values.tolist()
    return df_li


# 登录函数
def login(account, password):
    header = {
        "Origin": origin,
        "Referer": "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0",
        "User-Agent": user_agent,
        "Host": host,
    }
    post_url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login"
    post_data = {
        "uid": account,
        "upw": password,
        "smbtn": "进入健康状况上报平台",
        "hh28": "722",
    }
    response = session.post(post_url, data=post_data, headers=header)
    response.encoding = "utf-8"
    post_data = get_session_data(response.text)

# 获取登录的session信息
def get_session_data(html):
    print(html)
    r = re.search('ptopid=(.*)&sid=(.*)"', html)
    print(r)
    global info
    info[0] = r.group(1)
    info[1] = r.group(2)
    print(info)
    return info


# 查询核酸结果
def submit(data):
    url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/getzhbofmen"
    headers = {
        "User-Agent": user_agent,
        "Host": host,
        "Origin": origin,
    }
    params = {
        'ptopid': info[0],
        'sid': info[1]
    }
    r = requests.get(url, headers=headers, params=params)
    r.encoding = "utf-8"
    # soup = BeautifulSoup(r, "html.parser")
    a = time.strftime('%Y-%m-%d', time.localtime())
    b = r.text
    soup = BeautifulSoup(b, "html.parser")
    c = str(soup.head.script)
    print(c)
    res = re.search('核酸结果时间<br />(.*)</div><div style=\'width:20px;height:100%', c)
    d = str(res.group(1))
    return d


def hsjg(number, id_card):
    login(number, id_card)
    res = submit(data)
    result.append([number, res])


# main方法
if __name__ == "__main__":
    # 设置延迟时间（秒）
    s = 10
    # 设置账号密码路径文件
    path = "users.xls"

    all_users = read_users(path)
    for user in all_users:
        hsjg(user[0], str(user[1])[-8:])
        time.sleep(s)
    df = pd.DataFrame(result)
    # 保存到本地excel
    df.to_excel("result.xls", index=False)
