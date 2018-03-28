import json

import requests

from .settings import PROXY_API_URL, PROXY_API_TIMEOUT


def get_proxy_ip(order_no):
    """
    请求无忧代理IP获取API地址，返回新的IP

    这里使用的是无忧IP代理，官网：http://www.data5u.com/，你也可以使用其他的IP代理方案，
    自己实现一个返回新的IP的函数即可

    :param order_no: 无忧IP代理订单号
    """
    api_url = PROXY_API_URL + order_no
    with requests.Session() as s:
        response = s.get(api_url, timeout=PROXY_API_TIMEOUT).text.strip()
    # 订单号不存在
    if 'false' in response:
        error = json.loads(response)
        raise ValueError(error['msg'])

    return 'http://' + response
