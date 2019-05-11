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
from data.activitydata import ActivityData


class UserData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()
		self.activity = ActivityData()

	# 会员数据获取（等级划分、成长值规则、会员等级情况）
	def vip_data(self, model):
		file_path = "/public/yaml/user/vip_data.yaml"
		ret = self.get_config_data.get_data_post("getVipLevel", file_path)
		url = ret['url']
		header = ret['header']
		data = {"cases_text": "会员数据"}

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == "fail":
			return 500

		# 特殊断言
		report = ""
		if params['data']['growthRule']['money'] < 0 or params['data']['growthRule']['growth'] < 0:
			params['report_status'] = 202
			report += '会员成长值和消费值不能小于0,growthRule=' + str(params['data']['growthRule'][
															 'money']) + ";growth=" + str(
					params['data']['growthRule']['growth']) + "<br/>"

		if params['data']['levelRule']:
			for level_rule in params['data']['levelRule']:
				if level_rule['integral'] < 0:
					params['report_status'] = 202
					report += '会员等级门槛不能小于0，integral=' + str(level_rule['integral']) + "<br/>"
				if level_rule['discount'] < 0 or level_rule['discount'] > 10000:
					params['report_status'] = 202
					report += '会员折扣不正确，discount=' + str(level_rule['discount']) + "<br/>"
		else:
			report += '会员等级不能为空' + "<br/>"

		result_status['report'] = report
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 用户详情
	def info(self, model):
		file_path = "/public/yaml/user/info.yaml"
		ret = self.get_config_data.get_data_post("getUserInfo", file_path)
		url = ret['url']
		header = ret['header']
		data = {'cases_text': "用户详情"}
		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == 'fail':
			return 500

		# 特殊断言
		report = ""
		if int(params['data']['uid']) != int(header['uid']):
			params['report_status'] = 204
			report += '获取用户信息错误，uid=' + str(params['data']['uid'])

		result_status['report'] = report
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params['data']

	# 获取星座列表数据
	def star_sign(self, model):
		file_path = "/public/yaml/user/star_sign.yaml"
		ret = self.get_config_data.get_data_post("getStarSignList", file_path)
		url = ret['url']
		header = ret['header']
		data = {"cases_text": "星座列表"}

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		# 判断status
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == "fail":
			return 500

		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 用户充值明细
	def recharge(self, model):
		file_path = "/public/yaml/user/recharge.yaml"
		ret = self.get_config_data.get_data_post("getRechargeDetail", file_path)
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
				for request_data in params['data']['list']:
					if request_data['amount'] < 0:
						params['report_status'] = 202
						report += "充值记录中充值金额不能小于0,充值id=" + str(request_data['id']) + ";amount=" + str(
								request_data['amount']) + "</br>"
					if request_data['extend']['give'] < 0:
						params['report_status'] = 202
						report += "充值记录中赠送金额不能小于0,充值id=" + str(request_data['id']) + ";give=" + str(
								request_data['extend']['give']) + "</br>"

			result_status['report'] = report
			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 用户消费数据列表
	def spending(self, model):
		file_path = "/public/yaml/user/spending.yaml"
		ret = self.get_config_data.get_data_post("getSpendingInfo", file_path)
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
			for result_data in params['data']['list']:
				if data['type'] != 0 and result_data['type'] != data['type']:
					params['report_status'] = 202
					report += "消费明细类型错误，type=" + str(result_data['type']) + "<br/>"
				if not result_data['orderId']:
					params['report_status'] = 202
					report += "使用订单不能为空，orderId= " + str(result_data['orderId']) + "<br/>"

			result_status['report'] = report
			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 充值统计数据
	def recharge_amount(self, model):
		file_path = "/public/yaml/user/recharge_amount.yaml"
		ret = self.get_config_data.get_data_post("getRechargeCount", file_path)
		url = ret['url']
		header = ret['header']
		data = {"cases_text": "充值统计数据"}

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == 'fail':
			return 500

		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 充值
	def vip_recharge(self, model):
		file_path = "/public/yaml/user/vip_recharge.yaml"
		ret = self.get_config_data.get_data_post("postRecharge", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		for data in post_data:
			# 获取充值参数
			recharge_list = self.activity.recharge_list(model)
			recharge_data = random.choice(recharge_list)

			data['amount'] = recharge_data['amount']
			data['give'] = recharge_data['give']
			data['id'] = recharge_data['id']
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				return 500

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 用户赠送数据列表
	def give(self, model):
		file_path = "/public/yaml/user/give.yaml"
		ret = self.get_config_data.get_data_post("getUserGiveList", file_path)
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
					if result_data['extend']['money'] < 0 or not result_data['extend']['fromUid']:
						params['report_status'] = 202
						report += "邀请返还金额和被邀请人id数据不对，money=" + str(result_data['extend']['money']) + ";fromUid=" + \
								  str(result_data['extend']['fromUid']) + "<br/>"
			else:
				report += "没有数据"

			result_status['report'] = report
			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 店铺会员初始化
	def init_shop(self, model):
		file_path = "/public/yaml/user/init_shop.yaml"
		ret = self.get_config_data.get_data_post("initUserShop", file_path)
		url = ret['url']
		header = ret['header']
		data = {'cases_text': "店铺会员初始化"}

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == 'fail':
			return 500

		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 获取联系人电话
	def picked_up_info(self):
		file_path = "/public/yaml/user/picked_up_info.yaml"
		ret = self.get_config_data.get_data_post("getUserSelfMobile", file_path)
		# 组装请求数据
		url = ret['url']
		header = ret['header']
		data = []
		result = 200

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, ['订单', '联系人'], data)  # 判断status
		if result_status == 'fail':
			return 500

		self.get_yaml_data.set_to_yaml(ret, data, params, ['订单', '联系人'], result_status)

		return params

	# 我的钱包-账号余额统计
	def balance(self, model):
		file_path = "/public/yaml/user/balance.yaml"
		ret = self.get_config_data.get_data_post("getAccountBalance", file_path)
		url = ret['url']
		header = ret['header']
		data = {"cases_text": "钱包"}

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == 'fail':
			return 500

		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 注册获取验证嘛，并提交
	def code_receive(self, model):
		num = random.randint(1, 10)
		if num != 5:
			return True

		file_path = "/public/yaml/user/vip_code.yaml"
		ret = self.get_config_data.get_data_post("getUserCode", file_path)
		url = ret['url']
		header = ret['header']
		data = ret['expect']['retData']

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == 'fail':
			return 500

		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params


if __name__ == '__main__':
	run = UserData()
	ret = run.code_receive()
	print(ret)
