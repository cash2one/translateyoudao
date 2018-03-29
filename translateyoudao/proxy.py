import weakref
from threading import Thread
from time import sleep


class ProxiesDict(dict):
    """方便弱引用"""
    pass


def flush_proxies(func, args, proxies, sleep_time):
    """
    定时切换代理IP，改变已经存在IP代理字典对象

    :param
        func: 获取代理IP的函数，可以自己实现
        args: 获取代理IP函数所需参数，list或tuple
        proxies: IP代理字典对象
    """
    while True:
        sleep(sleep_time)
        proxy_ip = func(*args)
        try:
            proxies['https'] = proxies['http'] = proxy_ip
        # 代理IP字典对象已被销毁，终止切换代理IP
        except ReferenceError:
            break


def get_proxies(func, args=None, sleep_time=5):
    """
    根据所传入的获取代理IP函数获取代理IP，并构造requests所需格式的IP代理字典，
    并另起一个守护线程每隔一段时间更新一次IP代理。

    :param
        func: 获取代理IP的函数，可以自己实现
        args: 获取代理IP函数所需参数，list或tuple
        sleep_time: 刷新IP代理的间隔时间，默认5秒
    """
    if args is None:
        args = ()

    proxy_ip = func(*args)
    proxies = ProxiesDict(http=proxy_ip, https=proxy_ip)
    # 使用弱引用代理对象，防止内存泄露
    proxies_proxy = weakref.proxy(proxies)
    t1 = Thread(target=flush_proxies, args=(func, args, proxies_proxy, sleep_time), daemon=True)
    t1.start()

    return proxies
