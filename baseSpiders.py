#coding:utf-8
#auth:JyHu


import requests
from urllib import urlopen
import re
import sys
import os


'''
  >>> import requests
       >>> r = requests.get('https://www.python.org')
       >>> r.status_code
       200
       >>> 'Python is a programming language' in r.content
       True
    
    ... or POST:
    
       >>> payload = dict(key1='value1', key2='value2')
       >>> r = requests.post('http://httpbin.org/post', data=payload)
       >>> print(r.text)
       {
         ...
         "form": {
           "key2": "value2",
           "key1": "value1"
         },
         ...
       }
'''

class baseSpider:
	def __init__(self, root_path, charset = 'utf-8'):
		self.root_path = root_path
		self.charset = charset
		self.make_folder(root_path)

	charset_pat = r'<meta.*?charset=[\"\']?(.*?)[\"\']>'

	# 抓取网页中的数据，并根据正则表达式返回匹配的结果
	# page_url	页面地址
	# re_pat	正则表达式
	def load_web_page(self, page_url, re_pat):
		r = requests.get(page_url)
		print re_pat
		if r.status_code == 200:
			cs = re.compile(self.charset_pat).findall(r.content)
			if cs[0] and len(cs[0]) > 0: self.charset = cs[0]
			syscode = sys.getfilesystemencoding()
			text = r.content.decode(self.charset, 'ignore').encode(syscode)
			# print re_pat
			res = re.compile(re_pat).findall(text)
			print res
		else:
			return []

	# 创建一个文件夹，避免重建
	def make_folder(self, folder_path):
		try: os.mkdir(folder_path)
		except Exception, e: print e 





if __name__ == '__main__':
	bs = baseSpider('test')
	testPat = "<td><a\\s+target=\"_blank\"\\s+href=\"(.*?)\">(.*+)[\\s\\S]*?</a></td>"
	rs = bs.load_web_page('http://sc.eywedu.com/apple.asp?id=6&page=2', testPat)
	for r in rs:
		print r[0]

