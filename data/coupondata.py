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
from data.orderdata import OrderData


class CouponData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()
		self.order = OrderData()

	# 获取活动配置-注册弹窗信息
	def get_reg(self, model):
		file_path = "/public/yaml/activity/get_reg.yaml"
		ret = self.get_config_data.get_data_post("getRegConfigInfo", file_path)
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

	# 领取中心
	def coupon_center(self, model):
		file_path = "/public/yaml/activity/coupon_center.yaml"
		ret = self.get_config_data.get_data_post("getCouponCenterList", file_path)
		url = ret['url']
		header = ret['header']
		data = []

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)

		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == "fail":
			return 500
		report = ""
		if params['data']:
			for request_data in params['data']:
				if request_data['amount'] < 0:
					params['report_status'] = 202
					report += '优惠金额不能小于0，amount=' + str(request_data['amount']) + "</br>"

		result_status['report'] = report
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 获取用户邀请比例
	def coupon_get_invite_rebate(self, model):
		file_path = "/public/yaml/activity/coupon_get_invite_rebate.yaml"
		ret = self.get_config_data.get_data_post("getInviteRebate", file_path)
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
			# 特殊断言
			report = ""
			if params['data']['firstRatio'] < 0 or params['data']['firstRatio'] > 10000:
				params['report_status'] = 202
				report += '首次邀请奖励比例不正确，ratio=' + str(params['data']['firstRatio']) + "</br>"
			if params['data']['ratio'] < 0 or params['data']['ratio'] > 10000:
				params['report_status'] = 202
				report += '邀请奖励比例不正确，ratio=' + str(params['data']['ratio']) + "</br>"

			result_status['report'] = report
			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 我的优惠券列表
	def coupon_list(self, model, post_data = None):
		file_path = "/public/yaml/activity/coupon_list.yaml"
		ret = self.get_config_data.get_data_post("getMyCouponList", file_path)
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
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 优惠券使用总计优惠金额
	def coupon_used_amount(self, model):
		file_path = "/public/yaml/activity/coupon_used_amount.yaml"
		ret = self.get_config_data.get_data_post("getCouponUsedAmount", file_path)
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

	# 获取分享优惠券地址
	def coupon_get_share(self, model, post_data = None):
		file_path = "/public/yaml/activity/coupon_get_share.yaml"
		ret = self.get_config_data.get_data_post("getShareCoupon", file_path)
		url = ret['url']
		header = ret['header']
		if not post_data:
			post_data = ret['expect']['retData']

		# 获取订单
		order_list = self.order.list(model, [{"status": [9], "page": 1, "size": 10, "refundType": []}])
		order_one = random.choice(order_list['data']['list'])

		# 循环用例，请求获取数据
		for data in post_data:
			if data['orderId']:
				data['orderId'] = order_one['id']

			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == "fail":
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 获取邀请优惠券信息
	def get_invitations(self, model):
		file_path = "/public/yaml/activity/coupon_get_invitations.yaml"
		ret = self.get_config_data.get_data_post("getInvitationsInfo", file_path)
		url = ret['url']
		header = ret['header']
		data = []

		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == "fail":
			return 500

		report = ""
		if not params['data']:
			report += "没有邀请优惠券信息"

		result_status['report'] = report
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 获取邀请奖励规则数据
	def coupon_invitations_rule(self, model):
		file_path = "/public/yaml/activity/coupon_invitations_rule.yaml"
		ret = self.get_config_data.get_data_post("getInvitationsRule", file_path)
		url = ret['url']
		header = ret['header']
		data = []

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)

		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == "fail":
			return 500

		# 写入html
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 获取邀请奖励比例和邀请返券
	def check_invite_conf(self, model):
		file_path = "/public/yaml/activity/check_invite_conf.yaml"
		ret = self.get_config_data.get_data_post("isCashBack", file_path)
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

	# 惠券使用-可用券列表
	def coupon_able_list(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/activity/coupon_able_list.yaml"
		ret = self.get_config_data.get_data_post("getAvailableCoupon", file_path)
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

		return params['data']

	# 菜品券-首次发券选择可发券列表
	def coupon_goods_able_list(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/activity/coupon_goods_able_list.yaml"
		ret = self.get_config_data.get_data_post("getCouponGoodsList", file_path)
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

		return params

	# 赠券
	def coupon_donate(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/activity/coupon_donate.yaml"
		ret = self.get_config_data.get_data_post("coupongiving", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 获取可赠送的优惠券
			res = self.coupon_list(model, [{"type": 1, "page": 1}])
			choice_coupon = ""
			for coupon_data in res['data']['list']:
				if coupon_data['allowGive'] == 1:
					choice_coupon = coupon_data
					break
			if not choice_coupon:
				result_status = {"key": [], "val": [], 'report': ""}
				res['message'] = "没有可以分享的优惠券"
				self.get_yaml_data.set_to_yaml(ret, data, res, model, result_status)
				continue
			data['id'] = choice_coupon['id']
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == "fail":
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 检查当前用户是否已领取分享券
	def check_receive_share(self, model, post_data = None):
		# 获取文件请求数据
		file_path = "/public/yaml/activity/check_receive_share.yaml"
		ret = self.get_config_data.get_data_post("checkReceiveShare", file_path)
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

		return True

	# 检查当前用户是否已领取分享券
	def receive_share(self, model, post_data = None):
		# 获取文件请求数据
		file_path = "/public/yaml/activity/receive_share.yaml"
		ret = self.get_config_data.get_data_post("getReceiveShare", file_path)
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
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 检查当前用户是否已领取分享券
	def lucky_share(self, model, post_data = None):
		# 获取文件请求数据
		file_path = "/public/yaml/activity/lucky-share.yaml"
		ret = self.get_config_data.get_data_post("getLuckyShare", file_path)
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
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 领取红包雨
	def get_share_coupon(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/activity/lucky_share.yaml"
		ret = self.get_config_data.get_data_post("getLuckyShare", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 获取订单列表
			order_list = self.order.list(model, [{"status": [9], "size": 3}])
			order_one = random.choice(order_list['data']['list'])

			# 获取分享的code
			share_code = self.coupon_get_share(model, [{"orderId": order_one['id']}])
			url_code = share_code['data']['url']
			# 截取code
			code_data = url_code.split('=')
			code = code_data[len(code_data) - 1]

			# 检查当前用户是否已领取此分享券
			check_share = self.check_receive_share(model, [{"code": code}])
			if check_share == 500:
				continue

			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == "fail":
				continue

			# 获取已领取的分享优惠券信息
			self.receive_share(model, [{"code": code}])

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True


if __name__ == '__main__':
	run = CouponData()
	ret = run.get_share_coupon(['优惠券', '优惠券'])
	print(ret)