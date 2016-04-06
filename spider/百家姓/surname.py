# coding:utf-8
# auth:JyHu


import sys
sys.path.append('../..')
from abstract import *


# http://www.eywedu.com/baijiaxing/cy.asp?id=123


list_re = "<a\\s+href=\"(show.asp\\?id=[\\d]+?)\".*?>(.*?)</a>"
root_folder = "history_today"
errors_collect = []



def save_surname(surname, filepath):
	sur_list = load_web_page("http://www.eywedu.com/baijiaxing/cyshow.asp?id=%s" % surname[0], "<td\\s+align=\"left\"\\s+bgcolor=#FFFFFF>([\\s\\S.]+?)</td>")
	text = replace_white_space(sur_list[0])
	if text and len(text) > 0:
		print "保存 %s 成功" % filepath
		with open(filepath, 'w') as f:
			f.write(text)
	else:
		print "\n\n"
		print "保存 %s 失败" % filepath

def load_surnames():
	make_folder("surname")
	for page in range(1, 6):
		sur_url = 'http://www.eywedu.com/baijiaxing/index.asp?page=%d&fl1=&fl2=' % page
		surname_list = load_web_page(sur_url, "<td\\s+width=10%><a\\s+href=javascript:cy\\('(\\d+?)'\\)>(.*?)</a></td>")
		for surname in surname_list:
			filepath = "surname/%s-%s.txt" % (surname[0], surname[1])
			try:
				if not os.path.exists(filepath):
					save_surname(surname, filepath)
				else:
					print "%s已经存在" % filepath
			except Exception, e:
				print e
				save_surname(surname, filepath)

if __name__ == "__main__":
	load_surnames()

