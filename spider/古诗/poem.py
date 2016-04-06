# coding:utf-8
# auth:JyHu

import sys
sys.path.append('../..')
from baseSpider import baseSpider
import re

# http://sc.eywedu.com	诗词首页
# http://sc.eywedu.com/apple.asp?id=6&page=2	诗人列表
# http://sc.eywedu.com/orange.asp?id=4674&page=2	查看诗人的诗列表
# http://sc.eywedu.com/banana.asp?id=7357
# http://sc.eywedu.com/orange.asp?id=4636&page=1banana.asp?id=713

class poem_spider(baseSpider):

	authorURL = 'http://sc.eywedu.com/apple.asp?id=6&page='	# 诗人列表的地址
	authorPat = "<td><a\\s+target=\"_blank\"\\s+href=\"(.*?)\">(.*?)</a></td>"	# 获取诗人列表的正则
	basePoemsURL = 'http://sc.eywedu.com/'	# 根地址
	detail_pat = '<strong>(.*?)</strong></td>[\\s\\S]*?<td>([\s\S.]*?)</td>'	# 获取详情的正则

	dynasty_list = {
					'汉' : '2',
					'魏晋' : '3',
					'南北朝' : '4',
					'隋' : '5',
					'唐' : '6',
					'宋' : '7',
					'辽' : '9',
					'金' : '10',
					'元' : '8',
					'明' : '11',
					'清' : '12',
					'现当代' : '13',
					'不详' : '14'
					}

	def __init__(self, base_folder):
		baseSpider.__init__(self, base_folder)
		self.base_folder = base_folder	# 存放抓取到的内容的根地址
		for key, value in self.dynasty_list.items():
			dynasty_folder = "%s/%s" % (self.base_folder, key)
			self.make_folder(dynasty_folder)
			self.load_authors("http://sc.eywedu.com/apple.asp?id=%s&page=" % value, dynasty_folder)

	# 抓取所有的诗人
	def load_authors(self, authors_url, dynasty_folder):
		page = 1	# 分页
		while True:
			authorList = self.load_web_page('%s%d' % (authors_url, page), self.authorPat)	# 当前分页页面诗人列表
			if len(authorList) > 0:			# 如果抓取到的数据存在
				for author in authorList: self.load_poems(author, dynasty_folder)	# 遍历所有诗人，然后读取作品列表
				if len(authorList) < 120: break		# 因为每页为120个，超过了就是最后一页了
			else: break
			page += 1

	# 抓取当前诗人所有的作品
	def load_poems(self, author, dynasty_folder):
		auth_folder = "%s/%s" % (dynasty_folder, author[1].strip())
		self.make_folder(auth_folder)	# 为每位诗人创建一个文件夹
		a_page = 1	# 分页页码
		while True:
			poems_url = '%s%s&page=%d' % (self.basePoemsURL, author[0].strip(), a_page)
			poems_list = self.load_web_page(poems_url, self.authorPat)	# 作品列表
			if len(poems_list) > 0:
				for poem in poems_list:	self.save_poems(poem, auth_folder)		# 遍历诗人的所有作品，然后保存下来
				if len(poems_list) < 120: break
			else: break
			a_page += 1

	def save_poems(self, poem, auth_folder):
		poem_path = ("%s/%s.txt" % (auth_folder, re.sub(r'/', '·', poem[1].strip())))
		if not self.check_file_exists(poem_path):	# 如果文件不存在，再去请求作品的内容，这样可以节省时间
			detail_list = self.load_web_page("%s%s" % (self.basePoemsURL, poem[0].strip()), self.detail_pat)
			print poem_path
			if len(detail_list) > 0:
				poem_detail = ''
				for detail in detail_list:		# 遍历所有匹配的内容，然后拼接成一首完整的诗的内容
					poem_detail += detail[1]
					poem_detail += '\n'
				with open(poem_path, 'w') as f: f.write(self.replace_white_space(poem_detail))	# 保存到本地
			else: self.error_message('读取到空内容 %s' % poem_path)

if __name__ == '__main__':
	spider = poem_spider('poem')
