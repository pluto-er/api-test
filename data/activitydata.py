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


class ActivityData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()

	# 获取充值活动列表
	def recharge_list(self, model):
		file_path = "/public/yaml/activity/recharge_list.yaml"
		ret = self.get_config_data.get_data_post("getRechargeList", file_path)
		url = ret['url']
		header = ret['header']
		data = []

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == "fail":
			return 500

		# 特殊断言
		report = ""
		for result_data in params['data']:
			if result_data['isEnable'] != 1:
				params['report_status'] = 202
				report += "已禁用的数据不应该返回,id=" + str(result_data['id']) + ";isEnable=" + str(
						result_data['isEnable']) + "<br/>"
			if result_data['amount'] <= 0:
				params['report_status'] = 202
				report += "充值金额不能小于等于0,id=" + str(result_data['id']) + ";amount=" + str(result_data['amount']) + "<br/>"
			if result_data['give'] < 0:
				params['report_status'] = 202
				report += "赠送金额不能小于0,id=" + str(result_data['id']) + ";amount=" + str(result_data['amount']) + "<br/>"

		result_status['report'] = report
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params['data']

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

			result_status = self.validator.validate_status(ret['expect'], params)
			if result_status == 'fail':
				result = 500
				self.get_html_data.set_html('用户地址', url, data, result, params['message'], '新增用户地址失败')
			# 写入html
			self.get_html_data.set_html('用户地址', url, data, result, params['message'], '')

		return result

	# 删除配送地址
	def delete(self):
		# 获取文件请求数据
		file_path = "/public/yaml/user/address_delete.yaml"
		ret = self.get_config_data.get_data_post("getRechargeList", file_path)

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
			result_status = self.validator.validate_status(ret['expect'], params)
			if result_status == 'fail':
				result = 500
				self.get_html_data.set_html('用户地址', url, data, result, params['message'], '删除用户地址失败')

			# 写入html
			self.get_html_data.set_html('用户地址', url, data, result, params['message'], '')

		return result


if __name__ == '__main__':
	run = ActivityData()
	ret = run.recharge_list()
	print(ret)
