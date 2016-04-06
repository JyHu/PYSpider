# coding:utf-8
# auth:JyHu


import sys
sys.path.append('../..')
from baseSpider import baseSpider


class ClassicOfPoetry(baseSpider):

	poetryList = {	'风' : 'index2.htm',
					'雅' : 'index3.htm',
					'颂' : 'index4.htm'}

	poetryBaseURL = 'http://www.xiexingcun.com/shijing/'
	poetryListPat = "<img\\s+src=.*?align=.*?>\\s*?<A\\s+HREF=\"(.*?)\"\\s+>(.*?)</A><BR>"
	poetryDetailPat = '<p\\s+align=\"left\">.*?<div\\s+align=center>.*?</div><!--HTMLBUILERPART0--><DIV.*?>.*?</DIV>([\\s\\S.]*?)<!--/HTMLBUILERPART0-->.*?</p>'

	def __init__(self, base_folder):
		baseSpider.__init__(self, base_folder)
		self.base_folder = base_folder
		for key, value in self.poetryList.items():
			poetryFolder = "%s/%s" % (base_folder, key)
			self.make_folder(poetryFolder)
			poetries = self.load_web_page("%s/%s" % (self.poetryBaseURL, value), self.poetryListPat)
			for poetry in poetries:
				file_path = "%s/%s.txt" % (poetryFolder, poetry[1].strip())
				if not self.check_file_exists(file_path):
					details = self.load_web_page("%s/%s" % (self.poetryBaseURL, poetry[0]), self.poetryDetailPat)
					print "成功读取：", file_path
					with open(file_path, 'w') as f:
						f.write(self.replace_white_space(details[0]))

if __name__ == '__main__' :
	poetry = ClassicOfPoetry('ClassicPoetry')

