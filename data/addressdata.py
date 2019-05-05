# coding:utf-8
import sys
import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from helper.get_yaml import GetYaml
from helper.get_html import GetHtml
from helper.request_post import SendPost
from helper.validator import ValidatorHelper
from helper.get_config import GetDataConfig


class AddressData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()

	# 获取配送地址列表
	def list(self):
		# 获取文件请求数据
		file_path = "/public/yaml/user/address_list.yaml"
		ret = self.get_config_data.get_data_post("getUserAddress", file_path)
		# 组装请求数据
		url = ret['url']
		header = ret['header']
		data = []
		# 循环用例，请求获取数据
		result = 200
		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		# 判断status
		self.validator.validate_status(ret['expect'], params, '用户地址', url, data)

		# 写入html
		self.get_html_data.set_html('用户地址', url, data, result, params['message'], '')

		return params

	# 修改配送地址
	def update(self):
		# 获取文件请求数据
		file_path = "/public/yaml/user/address_update.yaml"
		ret = self.get_config_data.get_data_post("editAddress", file_path)
		# 组装请求数据
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			result = 200
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)

			# 判断status
			self.validator.validate_status(ret['expect'], params, '用户地址', url, data)

			# 写入html
			self.get_html_data.set_html('用户地址', url, data, result, params['message'], '')

		return result

	# 新增配送地址
	def add(self):
		# 获取文件请求数据
		file_path = "/public/yaml/user/address_add.yaml"
		ret = self.get_config_data.get_data_post("addUserAddress", file_path)

		# 组装请求数据
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			result = 200
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)

			self.validator.validate_status(ret['expect'], params, '用户地址', url, data)

			# 写入html
			self.get_html_data.set_html('用户地址', url, data, result, params['message'], '')

		return result

	# 删除配送地址
	def delete(self):
		# 获取文件请求数据
		file_path = "/public/yaml/user/address_delete.yaml"
		ret = self.get_config_data.get_data_post("delAddress", file_path)

		# 组装请求数据
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			result = 200
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)

			# 判断status
			self.validator.validate_status(ret['expect'], params, '用户地址', url, data)

			# 写入html
			self.get_html_data.set_html('用户地址', url, data, result, params['message'], '')

		return result


if __name__ == '__main__':
	run = AddressData()
	ret = run.delete()
	print(ret)
