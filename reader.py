# coding:utf-8
# auth:JyHu


import os, re, os

def read_with_path(path):
	os.system('clear')
	try:
		if os.path.exists(path):
			
			sub_items = os.listdir(path)
			
			sub_folders = []
			sub_files = []

			for item in sub_items:
				cur_path = "%s/%s" % (path, item)
				if os.path.isdir(cur_path):
					sub_folders.append(item)
				else:
					sub_files.append(item)

			show_item_list(sub_folders, sub_files, False, False)

			cur_index = -1

			while True:
				print '*' * 40
				print '\n(输入\'help\'或者\'h\'查看帮助)'
				selector = raw_input('\n            请输入你的选择 : ')
				os.system('clear')
				if not selector:
					cur_index = show_item_detail(sub_files, cur_index + 1, path)
				elif selector == 'b':
					break
				elif selector == 'lf':
					show_item_list(sub_folders, sub_files, True, False)
				elif selector == 'ld':
					show_item_list(sub_folders, sub_files, False, True)
				elif selector == 'l':
					show_item_list(sub_folders, sub_files, True, True)
				elif selector == 'help' or selector == 'h':
					show_help()
				elif selector == 'p':
					print path, '\n'
				elif selector[0:1] == 'f':
					if len(selector) > 0 and re.compile('^\d+$').match(selector[1:]):
						read_with_path("%s/%s" % (path, sub_folders[int(selector[1:])]))
					else:
						print '错误的指令，如需帮助，请输入\'help\'查看帮助\n'
				elif re.compile('^\d+$').match(selector):
					cur_index = show_item_detail(sub_files, int(selector), path)
				else:
					print '错误的指令，如需帮助，请输入\'help\'查看帮助\n'

	except Exception, e:
		print '\n\n', e, '\n遇到错误了', '\n当前路径', path, '\n\n'

def show_item_detail(sub_files, index, path):
	if len(sub_files) > 0 and len(sub_files) > index and index >= 0:
		print '\n', path
		print '当前第[%d]个' % index
		with open("%s/%s" % (path, sub_files[index])) as f:
			print '\n', '*' * 40, '\n\n', sub_files[index], '\n\n', f.read(), '\n\n'
		return index
	else:
		print '越界'
		print '处理后的索引', len(sub_files) - 1
		return show_item_detail(sub_files, len(sub_files) - 1, path)

def show_item_list(sub_folders, sub_files, full_lf, full_ld):
	if len(sub_folders) > 0:
		print '\n文件夹\n'
		max_index = len(sub_folders)
		if max_index > 20 and not full_lf: 
			max_index = 20
			print '(此处省略%d个文件夹目录，输入\'l\'查看更多目录)\n\n' % (len(sub_files) - 20)
		for i in range(0, max_index): print "[f%d] %s" % (i, sub_folders[i])
		print '\n\n'

	if len(sub_files) > 0:
		print '文件\n'
		max_index = len(sub_files)
		if max_index > 20 and not full_ld: 
			max_index = 20
			print '(此处省略%d个文件，输入\'l\'查看更多)\n\n' % (len(sub_files) - 20)
		for i in range(0, max_index): print "[%d] %s" % (i, sub_files[i])
		print '\n\n'

def show_help():
	print '以下为使用命令：'
	print 'help或者h : 查看帮助列表'
	print 'b : 返回上一级'
	print 'lf : 显示所有的目录'
	print 'ld : 显示所有的文件'
	print 'l : 显示所有的目录和文件'
	print 'p : 显示当前目录路径'
	print '输入\'f\'加数字选择显示的目录'
	print '输入数字选择显示的文件'
	print '\n\n'

if __name__ == '__main__':
	os.system('clear')
	print '\n\n\n\n'
	read_with_path(raw_input('请输入你想看的起始目录 : '))
# from __future__ import division

# import sys,time
# j = '#'
# if __name__ == '__main__':
#     for i in range(1,61):
#         j += '#'
#         sys.stdout.write(str(int((i/60)*100))+'% ||'+j+'->'+"\r")
#         sys.stdout.flush()
#         time.sleep(0.5)
# print


