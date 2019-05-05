# coding:utf-8
import sys
import os

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 获取根目录
sys.path.append(root_path)

from helper.get_yaml import GetYaml
from helper.get_html import GetHtml
from helper.request_post import SendPost
from helper.validator import ValidatorHelper
from helper.get_config import GetDataConfig


class ShopData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()

	# 获取评论列表
	def list(self):
		result = 200
		# 获取文件请求数据
		file_path = "/public/yaml/shop/city_list.yaml"
		ret = self.get_config_data.get_data_post("cityList", file_path)
		# 组装请求数据
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']
		ret_result = []

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)

			# 判断status
			result_status = self.validator.validate_status(ret['expect'], params)
			if result_status == 'fail':
				result = 500

			# 判断返回值的key和value
			print(params)
			exit()
			result_value = self.validator.validate_key_val(ret['expect'], params)
			print(result_value)
			exit()
			# 组装返回值
			data['result_data'] = result_status
			data['result_value'] = result_value
			ret_result.append(data)

			# 写入html
			msg = params['message']
			self.get_html_data.set_html(url, result_status, data, '评论', msg)

		# 写入结果yaml
		file_request_path = "/public/yaml/comment/list_request.yaml"
		self.get_yaml_data.set_to_yaml(file_request_path, ret_result)

		return result


if __name__ == '__main__':
	run = ShopData()
	run.list()
