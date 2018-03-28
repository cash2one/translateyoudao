"""
使用代理设置
"""
import re
from time import time

from translateyoudao.translate import translate
from translateyoudao.proxy import get_proxies
from translateyoudao.utils import get_proxy_ip

p = re.compile(r'[a-zA-Z]+')
text = """
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
"""
words = set(re.findall(p, text))

# 输入你购买的代理订单号
order_no = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# 获得代理对象，只需获取一次代理对象就行了，它会自动实现每隔5秒刷新一次代理IP
proxies = get_proxies(get_proxy_ip, args=(order_no, ))
# 建议一次不要传入太多单词
begin = time()
res = translate(*words, proxies=proxies)
end = time()
print('请求接口走了代理，以及有重试机制，所以速度稍慢')
print('用时: {}秒'.format(int(end - begin)))
success = 0
failed = 0
print('单词数: {}个'.format(len(words)))
for v in res.values():
    if v is not False:
        success += 1
    else:
        failed += 1

print('成功: {}个'.format(success))
print('失败: {}个'.format(failed))
