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


class UserCommentData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()

	# 用户评论奖励数据列表
	def comment_list(self, model):
		file_path = "/public/yaml/user/comment.yaml"
		ret = self.get_config_data.get_data_post("commentsRewardList", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == "fail":
				continue

			# 断言内容
			report = ""
			for result_data in params['data']['list']:
				if int(result_data['uid']) != int(header['uid']):
					params['report_status'] = 202
					report += "获取用户信息错误，uid=" + str(result_data['uid']) + "<br/>"

			result_status['report'] = report
			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 获取累计评论金额及用户消费评论总金额
	def comment_amount(self, model):
		file_path = "/public/yaml/user/comment_amount.yaml"
		ret = self.get_config_data.get_data_post("getCommentAmount", file_path)
		url = ret['url']
		header = ret['header']
		data = []

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == "fail":
			return 500

		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 我的评论-评论统计
	def comment_user_count(self, model):
		file_path = "/public/yaml/user/comment_user_count.yaml"
		ret = self.get_config_data.get_data_post("getCommentUserCount", file_path)
		url = ret['url']
		header = ret['header']
		data = []

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == "fail":
			return 500

		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True


if __name__ == '__main__':
	run = UserCommentData()
	ret = run.recharge_amount()
	print(ret)
