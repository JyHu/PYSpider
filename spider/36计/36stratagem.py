# coding:utf-8
# auth:JyHu

import sys
sys.path.append('../..')
from abstract import *


# http://ch.eywedu.com/36/index.html
# http://ch.eywedu.com/36/01.htm

stratagemPat = '第(\\d+)计\\s+<a\\s+target.*?href=\"(.*?)\">.*?>(.*?)</font></a>'
detailPat = '<td\\s+bgcolor=\"#EEECFF\"\\s+class=\"p141\">\\s+<.*?>([\\s\\S.]*?)</font></td>'

def save_36stratagem():
	make_folder('36stratagem')
	stratagemlist = load_web_page('http://ch.eywedu.com/36/index.html', stratagemPat)
	for stratagem in stratagemlist:
		detaillist = load_web_page('http://ch.eywedu.com/36/%s' % stratagem[1], detailPat)
		text = replace_white_space(detaillist[0])
		with open('36stratagem/第%s计-%s.txt' % (stratagem[0], stratagem[2]), 'w') as f:
			f.write(text)

if __name__ == "__main__":
	save_36stratagem()
