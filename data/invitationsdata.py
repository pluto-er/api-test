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


class InvitationsData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()

	# 我的钱包-邀请奖励金额统计
	def invitations_amount(self, model):
		file_path = "/public/yaml/user/invitations_amount.yaml"
		ret = self.get_config_data.get_data_post("getInvitationsAmount", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == "fail":
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 邀请消费人数统计 #按人数
	def invitations_by_count(self, model):
		file_path = "/public/yaml/user/invitations_by_count.yaml"
		ret = self.get_config_data.get_data_post("handelInvitationsUser", file_path)
		url = ret['url']
		header = ret['header']
		data = {"cases_text": "邀请消费人数统计"}

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status

		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 邀请奖励明细
	def invitations(self, model):
		file_path = "/public/yaml/user/invitations.yaml"
		ret = self.get_config_data.get_data_post("getInvitationsDetail", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				continue
			# 特殊断言
			report = ""
			if params['data']['list']:
				for result_data in params['data']['list']:
					if "extend" in result_data:
						if result_data['extend']['money'] < 0 or not result_data['extend']['fromUid']:
							params['report_status'] = 202
							report += "邀请返现金额和被邀请人id数据不对，money=" + str(result_data['extend']['money']) + ";fromUid=" + \
									  str(result_data['extend']['fromUid']) + "<br/>"
			else:
				report += "没有数据"
			result_status['report'] = report
			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 用户邀请奖励数据列表 #按人数
	def invitations_by(self, model):
		file_path = "/public/yaml/user/invitations_by.yaml"
		ret = self.get_config_data.get_data_post("getUserInvitations", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True


if __name__ == '__main__':
	run = InvitationsData()
	ret = run.invitations()
	print(ret)
