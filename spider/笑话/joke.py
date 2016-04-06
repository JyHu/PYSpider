# coding:utf-8
# auth:JyHu


import sys
sys.path.append('../..')
from baseSpider import baseSpider
import re


class joke(baseSpider):
	
	# http://xiaohua.zol.com.cn
	# <ul\s+class=\"news-list\s+classification-nav\s+clearfix\">([\s\S.]*?)</ul>
	# <a\s+target.*?href=\"(.*?)\">(.*?)<em>
	# 
	# http://xiaohua.zol.com.cn/lengxiaohua/
	# http://xiaohua.zol.com.cn/lengxiaohua/4.html
	# <li.*?article-summary\">[\s\S.]*?<span.*?article-title.*?href=\"(.*?)\">(.*?)</a>[\s\S.]*?</li>
	# 
	# http://xiaohua.zol.com.cn/detail46/45289.html
	# <div\s+class=\"article-text\">([\s\S.]*?)</div>

	baseJokeURL = 'http://xiaohua.zol.com.cn'
	categoryPat = '<ul\\s+class=\"news-list\\s+classification-nav\\s+clearfix\">([\\s\\S.]*?)</ul>'
	categoriesPat = '<a\\s+target.*?href=\"(.*?)\">(.*?)<em>'
	jokesListPat = '<li.*?article-summary\">[\\s\\S.]*?<span.*?article-title.*?href=\"(.*?)\">(.*?)</a>[\\s\\S.]*?</li>'
	jokeDetailPat = '<div\\s+class=\"article-text\">([\\s\\S.]*?)</div>'
	nextpagePat = '<a\\s+class=\"page-next\".*?href=\"(.+?)\">'

	def __init__(self, base_folder):
		baseSpider.__init__(self, base_folder, 'gbk')
		self.base_folder = base_folder
		self.load_categories_list()

	def load_categories_list(self):
		categories_str = self.load_web_page(self.baseJokeURL, self.categoryPat)
		if len(categories_str) > 0 and len(categories_str[0]) > 0:
			categories_list = re.compile(self.categoriesPat).findall(categories_str[0])
			if len(categories_list) > 0:
				for category in categories_list:
					page_next = category[0]
					category_path = "%s/%s" % (self.base_folder, category[1].strip())
					self.make_folder(category_path)
					while True:
						joke_list_html = self.load_web_source("%s%s" % (self.baseJokeURL, page_next))
						if len(joke_list_html) > 0:
							jokes_list = re.compile(self.jokesListPat).findall(joke_list_html)
							if len(jokes_list) > 0:
								for joke in jokes_list:
									if len(joke) >= 2:
										joke_path = "%s/%s.txt" % (category_path, joke[1].strip())
										if not self.check_file_exists(joke_path):
											joke_detail = self.load_web_page("%s%s" % (self.baseJokeURL, joke[0]), self.jokeDetailPat)
											print joke_path
											with open(joke_path, 'w') as f:
												f.write(self.replace_white_space(joke_detail[0]))
						next_find = re.compile(self.nextpagePat).findall(joke_list_html)
						if len(next_find) > 0 and len(next_find[0]) > 0:
							page_next = next_find[0]
							print category[1].strip(), page_next
						else: break

if __name__ == '__main__':
	j = joke('Joke')

