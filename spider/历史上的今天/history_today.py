# coding:utf-8
# auth:JyHu


import sys
import os
sys.path.append('../..')
from abstract import *

baseURL = 'http://ch.eywedu.com/today/'		# 跟地址
list_re = "<a\\s+href=\"(show.asp\\?id=[\\d]+?)\".*?>(.*?)</a>"	# 获取页面中内容数组的正则
detail_re = "<td><table.*?>([\\s\\S.]*?)</table></td>"	# 获取具体内容的正则
root_folder = "history_today"	# 保存文件的根目录
errors_collect = []	# 存储所有失败的数据

# http://ch.eywedu.com/today/show.asp?id=4529

# http://ch.eywedu.com/today/index.asp?today=0427


def save_today_news(today_info, folder_path):
	detail_list = load_web_page("%s%s" % (baseURL, today_info[0]), detail_re)
	if len(detail_list) > 0:
		text = replace_white_space(detail_list[0])
		if len(text) > 0:
			with open(folder_path, 'w') as f:
				f.write(text)

		else:
			error_info = error_message("抓取到了空的内容：%s\n地址是：%s\n名字是：%s")
			errors_collect.append(error_info)

def collect_history_today_news():
	make_folder(root_folder)
	ht_count = 0
	for month in range(1, 13):
		make_folder("%s/%02d" % (root_folder, month))
		for day in range(1, 32):
			folder_name = "%s/%02d/%02d" % (root_folder, month, day)
			make_folder(folder_name)
			news_list = load_web_page("%sindex.asp?today=%02d%02d" % (baseURL, month, day), list_re)
			with open("history_today_log.txt", 'a') as f: 
				f.write("\n")
				f.write("*" * 60)
				f.write("\n%02d月%02d日\n" % (month, day))
				f.write("\n")
			if len(news_list) > 0:
				for today_new in news_list:
					jfilepath = "%s/%s.txt" % (folder_name, today_new[1].strip())
					try:
						if not os.path.exists(jfilepath):
							print "已经抓取到%04d条内容，正在抓取%02d月%02d日的内容：%s" % (ht_count, month, day, today_new[1])
							with open("history_today_log.txt", 'a') as f: f.write("%s\n" % today_new[1])
							save_today_news(today_new, jfilepath)
							ht_count = ht_count + 1
						else:
							print "%s 文件已经存在" % jfilepath
					except Exception, e:
						print e
			elif day > 31: break

if __name__ == "__main__":
	collect_history_today_news()
	if len(errors_collect) > 0:
		for er in errors_collect:
			print er






