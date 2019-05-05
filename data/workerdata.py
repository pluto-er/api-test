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
from data.shopdata import ShopData


class WorkerData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()
		self.shop = ShopData()

	# 获取员工列表
	def list(self, model = []):
		file_path = "/public/yaml/worker/list.yaml"
		ret = self.get_config_data.get_data_post("workerList", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)
			if result_status == 'fail':
				continue

			# 特殊值断言
			report = ""
			if params['data']:
				# 断言管理着
				if params['data']['manager']:
					if params['data']['manager']['sid'] != header['sid']:
						report += str(params['data']['manager']['username']) + "(店长);uid=" + str(
								params['data']['manager']['uid']) + "不是本店铺员工，<br/>"
						params['report_status'] = 202
				else:
					report += '本店铺不存在店长<br/>'
				# 断言员工
				if params['data']['workerList']:
					for worker in params['data']['workerList']:
						if worker['sid'] != header['sid']:
							report += str(worker['username']) + ";uid=" + str(
									worker['uid']) + "不是本店铺员工，<br/>"
							params['report_status'] = 202
			else:
				report += "没有相关员工信息"

			result_status['report'] = report
			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 员工点赞，点踩或者取消点赞和点踩
	def evaluation(self, model):
		file_path = "/public/yaml/worker/evaluation.yaml"
		ret = self.get_config_data.get_data_post("workerEvaluation", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 获取员工列表
		worker = self.list(model)
		worker_list = []
		if worker['data']['manager']:
			worker_list.append(worker['data']['manager'])
		if worker['data']['workerList']:
			worker_list.append(random.choice(worker['data']['workerList']))
		if not worker_list:
			return 500

		# 循环用例，请求获取数据
		for data in post_data:
			for worker_data in worker_list:
				# 请求api获取结果
				data['workerId'] = worker_data['uid']
				params = self.send_post.send_post(url, data, header)
				result_status = self.validator.validate_status(ret, params, model, data)
				if result_status == 'fail':
					continue

				self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 打赏
	def reward_pay(self, model):
		# 获取员工列表
		worker = self.list(model)
		worker_list = []
		if worker['data']['manager']:
			worker_list.append(worker['data']['manager'])
		if worker['data']['workerList']:
			worker_list.append(random.choice(worker['data']['workerList']))
		if not worker_list:
			return False

		# 获取打赏列表
		reward = self.shop.reward_set(model)
		if not reward['data']:
			return False

		# 获取文件请求数据
		file_path = "/public/yaml/worker/reward_pay.yaml"
		ret = self.get_config_data.get_data_post("rewardPay", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData'][0]

		for data in worker_list:
			post_data['workerId'] = data['uid']
			post_data['rewardMoney'] = random.choice(reward['data'])
			params = self.send_post.send_post(url, post_data, header)
			result_status = self.validator.validate_status(ret, params, model, post_data)
			if result_status == 'fail':
				continue

			self.get_yaml_data.set_to_yaml(ret, post_data, params, model, result_status)

		return True


if __name__ == '__main__':
	run = WorkerData()
	ret = run.evaluation()
	print(ret)
