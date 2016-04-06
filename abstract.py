# coding:utf-8
# auth:JyHu

from urllib import urlopen
import re
import sys
import os

# 抓取网页中的数据，并根据正则表达式返回匹配的结果
# page_url	页面地址
# re_pat	正则表达式
def load_web_page(page_url, re_pat):
	print page_url
	webpage = urlopen(page_url)
	text = webpage.read()
	syscode = sys.getfilesystemencoding()
	text = text.decode('gb2312', 'ignore').encode(syscode)
	return re.compile(re_pat).findall(text)

# 创建一个文件夹，避免重建
def make_folder(folder_path):
	try: os.mkdir(folder_path)
	except Exception, e: print e 

# 替换文本内容中的空白字符
def replace_white_space(text):
	text = re.sub(r'<(BR|br)>', '\n', text)	# 替换html中的br换行符
	text = re.sub(r'<.*?>', '', text)		# 替换穿插在法律内容中的html标签对
	text = re.sub(r'&nbsp;', '', text)		# 替换html中的空白字符
	if len(text.strip()) == 0:
		return ""
	return text.strip()

def error_message(msg):
	sep_line = "*" * 60
	err = "\n%s\n\n%s\n\n%s\n" % (sep_line, msg, sep_line)
	print err
	return err

