# encoding=utf-8
import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录


class OperationHtml:

	def set(self, path, html):
		file_path = root_path + path
		f = open(file_path, 'w', encoding = "utf8")
		f.write(html)
		f.close()

	def set2(self, path, add_data):
		file_path = root_path + path
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

	def setold(self, path, add_data):
		file_path = root_path + path
		html = add_data
		f1 = open(file_path, 'rb')  # 打开yaml文件
		data = f1.read()
		data = str(data, encoding = 'utf-8')
		pos = data.find("<span></span>")
		ret_data = data[:pos] + html + data[pos:]
		f = open(file_path, 'w', encoding = "utf8")  # 打开yaml文件
		f.write(ret_data)
		f.close()
		f1.close()

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
	send_html = '{"className": "UiAutoTestCase111","methodName": "test_errors_save_imgs","description": "如果在测试过程中, 出现不确定的错误, 程序会自动截图, 并返回失败, 如果你需要程序自动截图, 则需要咋测试类中定义 save_img方法","spendTime": "7.78 s","status": "失败1","log": ["杀手大厦时家还是大家好"]},'
	ret = run.set("/public/html/sample.js", send_html)
	print(ret)
