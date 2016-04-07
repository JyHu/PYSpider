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

	charset_pat = r'<meta.*?charset=[\"\']*(.*?)[\"\']>'

	def __init__(self, root_path, charset = ''):
		self.root_path = root_path
		self.charset = charset
		self.make_folder(root_path)
		self.fortest = False

	# 抓取网页中的数据，并根据正则表达式返回匹配的结果
	# page_url	页面地址
	# re_pat	正则表达式
	def load_web_page(self, page_url, re_pat):
		if self.fortest: print page_url, '\n', re_pat
		text = self.load_web_source(page_url)
		if len(text) > 0: return re.compile(re_pat).findall(text)
		else: return []

	def load_web_source(self, page_url):
		if self.fortest: print page_url
		r = requests.get(page_url)
		if r.status_code == 200:
			if self.charset == '':
				cs = re.compile(self.charset_pat).findall(r.content)
				self.charset = 'utf-8'
				if len(cs) > 0 : 
					if len(cs[0]) > 0 : self.charset = cs[0]
			syscode = sys.getfilesystemencoding()
			text = r.content.decode(self.charset, 'ignore').encode(syscode)
			if self.fortest and len(text) > 0: print '成功获取页面内容\n'
			return text
		return ''

	# 创建一个文件夹，避免重建
	def make_folder(self, folder_path):
		try: os.mkdir(folder_path)
		except Exception, e: print "文件夹已经存在", folder_path

	def check_file_exists(self, file_path):
		try:
			if os.path.exists(file_path):
				print "文件已经存在", file_path
				return True
		except Exception, e: print "查看文件存在失败"

		return False

	def replace_white_space(self, text):
		if not text : return ''
		text = re.sub(r'<(BR|br)>', '\n', text)	# 替换html中的br换行符
		text = re.sub(r'<.*?>', '', text)		# 替换穿插在法律内容中的html标签对
		text = re.sub(r'(&nbsp;|&rdquo;|&hellip;|&ldquo;|&mdash;)', '', text)		# 替换html中的空白字符
		if len(text.strip()) == 0:
			return ""
		return text.strip()

	def error_message(self, msg):
		sep_line = "*" * 60
		err = "\n%s\n\n%s\n\n%s\n" % (sep_line, msg, sep_line)
		print err
		return err

	def test(self):
		bs = baseSpider('test')
		testPat = "<td><a\\s+target=\"_blank\"\\s+href=\"(.*?)\">(.+)[\\s\\S]*?</a></td>"
		rs = bs.load_web_page('http://sc.eywedu.com/apple.asp?id=6&page=2', testPat)
		if rs:
			for r in rs:
				print r[0], r[1], '\n'

