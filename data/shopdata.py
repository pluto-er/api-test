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


class ShopData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()

	# 城市列表
	def city_list(self, model = [], post_data = None):
		file_path = "/public/yaml/shop/city_list.yaml"
		ret = self.get_config_data.get_data_post("cityList", file_path)
		url = ret['url']
		header = ret['header']
		if post_data is None:
			post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)
			if result_status == 'fail':
				continue
			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params


if __name__ == '__main__':
	run = ShopData()
	run.city_list(['启动页', 'shezhi'])
