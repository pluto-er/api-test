# coding:utf-8
import sys
import os
import random

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from helper.get_yaml import GetYaml
from helper.get_html import GetHtml
from helper.request_post import SendPost
from helper.validator import ValidatorHelper
from helper.get_config import GetDataConfig
from data.workerdata import WorkerData
from data.userdata import UserData


class MsgData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()
		self.worker = WorkerData()
		self.user = UserData()

	# 获取每种通知类型最新数据和通知数量
	def detail(self, model):
		file_path = "/public/yaml/msg/detail.yaml"
		ret = self.get_config_data.get_data_post("getMessageCount", file_path)
		url = ret['url']
		header = ret['header']
		data = []

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)

		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == 'fail':
			return 500

		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 消息通知列表
	def list(self, model, post_data = None):
		file_path = "/public/yaml/msg/list.yaml"
		ret = self.get_config_data.get_data_post("getMessageList", file_path)
		url = ret['url']
		header = ret['header']
		if not post_data:
			post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == "fail":
				return 500

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 删除消息
	def delete(self, model):
		file_path = "/public/yaml/msg/delete.yaml"
		ret = self.get_config_data.get_data_post("delMessage", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 获取消息列表
			params = self.list(model, [{"type": random.randint(1, 6)}])
			if params == 500:
				continue

			if params['data']['list']:
				choice_data = random.choice(params['data']['list'])
			else:
				continue
			# 请求api获取结果
			data['id'] = choice_data['id']
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == "fail":
				return 500

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 获取用户IM信息
	def im_user_info(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/msg/im_user_info.yaml"
		ret = self.get_config_data.get_data_post("getIMUserInfo", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 获取店长
		worker = self.worker.list(model)
		if not worker['data']['manager']:
			return 500

		worker_manager = worker['data']['manager']['uid']
		# 获取当前用户用户中心id
		user = self.user.info(model)
		if user == 500:
			return 500

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			data['suid'] = worker_manager
			data['ucid'] = user['ucid']
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 获取用户IM信息记录
	def im_list(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/msg/im_list.yaml"
		ret = self.get_config_data.get_data_post("getOldIMMsg", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 获取店长
		worker = self.worker.list(model)
		if not worker['data']['manager']:
			return 500

		worker_manager = worker['data']['manager']['uid']
		# 获取当前用户用户中心id
		user = self.user.info(model)
		if user == 500:
			return 500

		# 循环用例，请求获取数据
		for data in post_data:
			data['toUid'] = worker_manager
			data['fromUid'] = user['ucid']
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 获取用户未读消息总数
	def push_count(self, model):
		file_path = "/public/yaml/msg/count.yaml"
		ret = self.get_config_data.get_data_post("getUnMsgDataNumber", file_path)
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
		if params['data']['num'] < 0:
			params['report_status'] = 202
			report += '消息总数不能为负，data=' + str(params['data']['num'])

		result_status['report'] = report
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True


if __name__ == '__main__':
	run = MsgData()
	ret = run.delete()
	print(ret)
