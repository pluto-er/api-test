# encoding=utf-8
# 操作HTML文件
import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录


class OperationHtml:
	"""
	# 写入数据到html文件
	# path 文件地址(相对/绝对位置)
	# html 写入内容
	"""

	def set(self, path, html):
		file_path = root_path + path
		f = open(file_path, 'w', encoding = "utf8")
		f.write(html)
		f.close()

	"""
		###############################分割线##################
	"""

	# 特殊写入文件
	def set2(self, path, add_data):
		file_path = path
		base_path = root_path + "/public/html/sample.html"
		f1 = open(base_path, 'rb')  # 打开yaml文件
		data = f1.read()
		data = str(data, encoding = 'utf-8')
		pos = data.find("//console.log('加载数据')")
		ret_data = data[:pos] + add_data + data[pos:]
		f = open(file_path, 'w', encoding = "utf8")  # 打开yaml文件
		f.write(ret_data)
		f.close()
		f1.close()

	# 开始文件
	def set_start(self, path):
		file_path = root_path + '/public/html/base.html'
		f1 = open(file_path, 'rb')  # 打开yaml文件
		data = f1.read()
		data = str(data, encoding = 'utf-8')
		file_path = root_path + path
		f = open(file_path, 'w', encoding = "utf8")  # 打开yaml文件
		f.write(data)
		f.close()
		f1.close()


if __name__ == '__main__':
	run = OperationHtml()
	run.set("/public/html/sample.html", "测试内容")
