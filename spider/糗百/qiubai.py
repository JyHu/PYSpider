# coding:utf-8



import sys
sys.path.append('../..')
from baseSpider import baseSpider
import re
import os


class qiubai(baseSpider):

	qb_url = 'http://www.qiushibaike.com'
	qb_pat = '<div\\s+class=\"content\">([\\s\\S.]*?)</div>'
	qb_npat = '<li>[\\s\\S]+<a\\s+href=\"(.*?)\"\s+rel=\".*?\">[\\s\\S]+<span\\s+class=\"next\">'

	def __init__(self, base_folder):
		baseSpider.__init__(self, base_folder)
		self.base_folder = base_folder
		self.load_qiubai(self.qb_url)

	def load_qiubai(self, purl):
		qb_html = self.load_web_source(purl)
		if len(qb_html) > 0:
			qb_list = re.compile(self.qb_pat).findall(qb_html)
			qb_next = re.compile(self.qb_npat).findall(qb_html)
			for qb in qb_list:
				print '\n\n', self.replace_white_space(qb), '\n'
				print '*' * 40
				raw_input('\n\n输入任何字符或者回车，查看下一条 ~ ')
				os.system('clear')
			if len(qb_next) > 0:
				self.load_qiubai("%s%s" % (self.qb_url, qb_next[0]))

if __name__ == '__main__':
	os.system('clear')
	qb = qiubai('qiubai')

