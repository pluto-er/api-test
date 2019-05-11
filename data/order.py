# coding:utf-8
import sys
import os
import time
import random
import json
import datetime

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from helper.get_config import GetDataConfig
from helper.get_premise import GetPremise
from helper.set_order import SetOrder
from helper.get_yaml import GetYaml
from helper.request_post import SendPost


class OrderData:

	def __init__(self):
		self.get_config_data = GetDataConfig()
		self.get_premise = GetPremise()
		self.set_order = SetOrder()
		self.get_yaml_data = GetYaml()
		self.send_post = SendPost()

	# 订单
	def add_order(self, type = 5):
		file_path = "/public/yaml/order/add.yaml"
		ret = self.get_config_data.get_data_post("postOrderUrl", file_path)
		pay_ret = {'data': {}, 'status': 500, 'code': 0, 'message': '接口报错', "request_time": 0, "traceid": 0}
		result_status = {"key": [], "val": [], 'report': ""}

		# 组合
		try:
			self.goods_type(type)
		except Exception as e:
			result_status['report'] = "组合" + str(e)
			self.get_yaml_data.set_to_yaml(ret, {}, pay_ret, ["订单", "下单"], result_status)

		# 套餐相关
		try:
			self.order_package(type)
		except Exception as e:
			result_status['report'] = "套餐相关" + str(e)
			self.get_yaml_data.set_to_yaml(ret, {}, pay_ret, ["订单", "下单"], result_status)

		# 加购
		try:
			self.add_goods(type)
		except Exception as e:
			result_status['report'] = "加购" + str(e)
			self.get_yaml_data.set_to_yaml(ret, {}, pay_ret, ["订单", "下单"], result_status)

		# 优惠券
		try:
			self.order_coupon(type)
		except Exception as e:
			result_status['report'] = "优惠券" + str(e)
			self.get_yaml_data.set_to_yaml(ret, {}, pay_ret, ["订单", "下单"], result_status)

		# 非营业时间
		try:
			self.business_time_out(type)
		except Exception as e:
			result_status['report'] = "非营业时间" + str(e)
			self.get_yaml_data.set_to_yaml(ret, {}, pay_ret, ["订单", "下单"], result_status)

		# 不支持自提
		try:
			self.shopping_way(type)
		except Exception as e:
			result_status['report'] = "非营业时间" + str(e)
			self.get_yaml_data.set_to_yaml(ret, {}, pay_ret, ["订单", "下单"], result_status)

		# 营业时间内-库存情况
		try:
			self.stock_ample(type)
		except Exception as e:
			result_status['report'] = "营业时间内-库存情况" + str(e)
			self.get_yaml_data.set_to_yaml(ret, {}, pay_ret, ["订单", "下单"], result_status)

	# 组合
	def goods_type(self, type):
		file_path = "/public/yaml/order/add.yaml"
		ret = self.get_config_data.get_data_post("postOrderUrl", file_path)
		# 0默认  1使用优惠券 2使用菜品券 3加购都选上
		term_text = ["", "-使用优惠券", "-加购不选"]
		for term in [0, 1, 2]:
			for post_status in [[2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]:
				data = self.set_order.get_base_data(type)  # 获取请求数据
				# 处理case描述
				if post_status == [2]:
					data['cases_text'] = "只购买多规格商品"
				elif post_status == [3]:
					data['cases_text'] = "只购买套餐商品"
				elif post_status == [1, 2]:
					data['cases_text'] = "购买单品和多规格"
				elif post_status == [1, 3]:
					data['cases_text'] = "购买单品和套餐"
				elif post_status == [2, 3]:
					data['cases_text'] = "购买多规格和套餐"
				elif post_status == [1, 2, 3]:
					data['cases_text'] = "购买单品、多规格、套餐"
				data['cases_text'] = data['cases_text'] + term_text[term]
				goods = self.get_premise.get_goods(type, post_status)
				if not goods:  # 没有值情况
					pay_ret = {'data': {}, 'status': 200, 'code': 0, 'message': '',
						"request_time": 0, "request_status": 202, "traceid": 0}
					result_status = {"key": [], "val": [], 'report': "没有数据，直接进行下一条件"}
					data['cases_text'] = self.get_type_code(type) + data['cases_text']
					self.get_yaml_data.set_to_yaml(ret, data, pay_ret, ["订单", "下单"], result_status)
				# 处理菜品
				goods_list_data = []
				price = vip_price = box_price = 0
				for goods_data in goods:
					if goods_data['isSale'] != 1:
						continue
					if goods_data['type'] == 1:
						goods_list = self.set_order.add_goods_type_single(goods_data, 1)  # 单品
					elif goods_data['type'] == 2:
						goods_list = self.set_order.add_goods_type_space(goods_data, 1)  # 多规格
					else:
						goods_list = self.set_order.add_goods_type_package(goods_data, 1)  # 套餐
					goods_list_data.append(goods_list)

					price = price + goods_list['price'] * goods_list['number']
					vip_price = vip_price + goods_list['vipPrice'] * goods_list['number']
					box_price = box_price + goods_list['boxPrice'] * goods_list['number']
				goods_params = {'goods': goods_list_data, 'price': price, 'vip_price': vip_price,
					"box_price": box_price}

				# 获取加购
				status = 0
				if term == 2:
					status = 3
				add_goods = self.get_premise.get_add_goods(type, status)

				# 组装数据
				goods_pay = self.set_order.get_pay_amount(type, goods_params, add_goods)
				data['goodsList'] = goods_pay['goodsList']
				data['addGoodsList'] = goods_pay['addGoodsList']
				data['price'] = goods_pay['price']
				data['vip_price'] = goods_pay['vip_price']
				if term == 1:
					# 优惠券
					coupon = self.get_premise.coupon_list()
					coupon_ret = self.set_order.validator_coupon(type, coupon, data['vip_price'], 1)
					if coupon_ret:
						coupon_one = random.choice(coupon_ret)
						data['couponIds'] = [coupon_one['id']]
						data['price'] = data['price'] - coupon_one['amount']
						data['vip_price'] = data['vip_price'] - coupon_one['amount']

				# 获取联系方式
				picked = 0
				if type == 4 or type == 5:
					picked = self.get_premise.picked_up_info()
				data['addressId'] = picked
				# 外卖地址
				if type == 3:
					address_data = self.set_order.set_shop_wm()
					data['addressId'] = address_data['address_id']
					data['price'] = data['price'] + address_data['service_fee']
					data['vip_price'] = data['vip_price'] + address_data['service_fee']
				pay_ret = self.pay(data, 2)
				pay_status = self.set_order.validator_pay(pay_ret, 2)
				report = ""
				if pay_status:
					time.sleep(1)
					cancel_status = self.cancel_order(pay_ret['data']['payment']['orderId'])
					if cancel_status:
						pay_ret = self.pay(data, 1)
						self.set_order.validator_pay(pay_ret, 1)
					else:
						report = "取消订单失败，orderId=" + str(pay_ret['data']['payment']['orderId'])

				result_status = {"key": [], "val": [], 'report': report}
				data['cases_text'] = self.get_type_code(type) + data['cases_text']
				self.get_yaml_data.set_to_yaml(ret, data, pay_ret, ["订单", "下单"], result_status)
				time.sleep(1)

		return True

	# 套餐相关
	def order_package(self, type):
		# 1必选单选/其他选1 2必选多选/其他选1 3 必选不选/其他选1
		# 4 非必单选（必选选择）  5非必选多选（必选选择） 6 非必选不选（必选选择）
		# coupon_data 1使用 2不使用
		coupon_text = ["-使用优惠券", ""]
		for coupon_data in [1, 2]:
			for post_status in [4, 5, 6]:
				file_path = "/public/yaml/order/add.yaml"
				ret = self.get_config_data.get_data_post("postOrderUrl", file_path)

				data = self.set_order.get_base_data(type)
				# 获取菜品
				goods = self.get_premise.get_package(type, post_status)
				# 获取加购
				add_goods = self.get_premise.get_add_goods(type)
				goods_pay = self.set_order.get_pay_amount(type, goods, add_goods)
				data['goodsList'] = goods_pay['goodsList']
				data['addGoodsList'] = goods_pay['addGoodsList']
				data['price'] = goods_pay['price']
				data['vip_price'] = goods_pay['vip_price']
				# 优惠券
				if coupon_data == 1:
					coupon = self.get_premise.coupon_list()
					coupon_ret = self.set_order.validator_coupon(type, coupon, data['vip_price'], 1)
					if coupon_ret:
						coupon_one = random.choice(coupon_ret)
						data['couponIds'] = [coupon_one['id']]
						data['price'] = data['price'] - coupon_one['amount']
						data['vip_price'] = data['vip_price'] - coupon_one['amount']

				# 获取联系方式
				picked = 0
				if type == 4 or type == 5:
					picked = self.get_premise.picked_up_info()
				data['addressId'] = picked
				if type == 3:
					address_data = self.set_order.set_shop_wm()
					data['addressId'] = address_data['address_id']
					data['price'] = data['price'] + address_data['service_fee']
					data['vip_price'] = data['vip_price'] + address_data['service_fee']
				pay_ret = self.pay(data, 2)
				result_status = self.set_order.validator_pay(pay_ret, 2)
				# 1必选单选/其他选1 2必选多选/其他选1 3 必选不选/其他选1
				# 4 非必单选（必选选择）  5非必选多选（必选选择） 6 非必选不选（必选选择）
				if post_status == 1:
					data['cases_text'] = "套餐内必选只选其一下单"
				elif post_status == 2:
					data['cases_text'] = "套餐内必选多选下单"
					pay_ret['status'] = 500
					pay_ret['message'] = "套餐内必选未选下单-却下单成功"
					if not result_status:
						pay_ret['status'] = 200
						pay_ret['code'] = 0
						pay_ret['message'] = ""
				elif post_status == 3:
					data['cases_text'] = "套餐内必选未选下单"
					pay_ret['status'] = 500
					pay_ret['message'] = "套餐内必选未选下单-却下单成功"
					if not result_status:
						pay_ret['status'] = 200
						pay_ret['code'] = 0
						pay_ret['message'] = ""
				elif post_status == 4:
					data['cases_text'] = "套餐内非必选选其一下单"
				elif post_status == 5:
					data['cases_text'] = "套餐内非必选多选下单"
				elif post_status == 6:
					data['cases_text'] = "套餐内非必选未选下单"
				report = ""
				if result_status:
					time.sleep(1)
					cancel_status = self.cancel_order(pay_ret['data']['payment']['orderId'])
					if cancel_status:
						pay_ret = self.pay(data, 1)
						self.set_order.validator_pay(pay_ret, 1)
					else:
						report = "取消订单失败，orderId=" + str(pay_ret['data']['payment']['orderId'])
				result_status = {"key": [], "val": [], 'report': report}
				data['cases_text'] = self.get_type_code(type) + data['cases_text']
				if coupon_data == 1:
					data['cases_text'] = data['cases_text'] + coupon_text[coupon_data - 1]
				self.get_yaml_data.set_to_yaml(ret, data, pay_ret, ["订单", "下单"], result_status)
				time.sleep(1)

		return True

	# 加购相关
	def add_goods(self, type, goods_type = [1]):
		file_path = "/public/yaml/order/add.yaml"
		ret = self.get_config_data.get_data_post("postOrderUrl", file_path)
		#  0 都选 1非必选不选	2必选不选 3非必选和必选都不选
		for post_status in [0, 1, 2, 3]:
			data = self.set_order.get_base_data(type)
			goods = self.get_premise.get_order_goods(type, [1], post_status)
			goods_pay = self.set_order.get_pay_amount(type, goods['goodsList'], goods['addGoodsList'])
			data['goodsList'] = goods_pay['goodsList']
			data['addGoodsList'] = goods_pay['addGoodsList']
			data['price'] = goods_pay['price']
			data['vip_price'] = goods_pay['vip_price']

			# 获取联系方式
			picked = 0
			if type == 4 or type == 5:
				picked = self.get_premise.picked_up_info()
			data['addressId'] = picked
			if type == 3:
				address_data = self.set_order.set_shop_wm()
				data['addressId'] = address_data['address_id']
				data['price'] = data['price'] + address_data['service_fee']
				data['vip_price'] = data['vip_price'] + address_data['service_fee']

			pay_ret = self.pay(data, 2)
			result_status = self.set_order.validator_pay(pay_ret, 2)
			if post_status == 0:
				data['cases_text'] = "加购产品满足条件"
				if not result_status:
					pay_ret['status'] = 500
			elif post_status == 1:
				data['cases_text'] = "不选非必选加购产品"
				if not result_status:
					pay_ret['status'] = 500
					pay_ret['code'] = 0
			elif post_status == 2:
				data['cases_text'] = "必选加购产品未选择"
				pay_ret['status'] = 500
				pay_ret['message'] = "必选加购产品未选择-却下单成功"
				if not result_status:
					pay_ret['status'] = 200
					pay_ret['code'] = 0
					pay_ret['message'] = ""
			elif post_status == 3:
				data['cases_text'] = "非必选加购商品和必选加购商品都不选"
				pay_ret['status'] = 500
				pay_ret['message'] = "非必选加购商品和必选加购商品都不选-却下单成功"
				if not result_status:
					pay_ret['status'] = 200
					pay_ret['code'] = 0
					pay_ret['message'] = ""
			report = ""
			# 余额支付
			if result_status:
				time.sleep(1)
				cancel_status = self.cancel_order(pay_ret['data']['payment']['orderId'])
				if cancel_status:
					pay_ret = self.pay(data, 1)
					self.set_order.validator_pay(pay_ret, 1)
				else:
					report = "取消订单失败，orderId=" + str(pay_ret['data']['payment']['orderId'])
			result_status = {"key": [], "val": [], 'report': report}
			data['cases_text'] = self.get_type_code(type) + data['cases_text']
			self.get_yaml_data.set_to_yaml(ret, data, pay_ret, ["订单", "下单"], result_status)
			time.sleep(1)
		return True

	# 优惠券
	def order_coupon(self, type = 5):
		file_path = "/public/yaml/order/add.yaml"
		ret = self.get_config_data.get_data_post("postOrderUrl", file_path)
		# coupon_status 1正常 2不在使用时间内 3就餐方式满足  4 就餐方式不满足 5金额满足 6金额不满足
		for post_status in [1, 2, 3, 4, 5, 6]:
			goods = self.get_premise.get_order_goods(type, [1])
			params_post = self.get_config_data.get_conf("getAvailableCoupon")
			coupon_list = self.send_post.send_post(params_post['url'], {}, params_post['header'])
			if coupon_list['status'] != 200 or not coupon_list['data'] or not coupon_list['data']['coupon']:
				return False
			coupon_data = coupon_list['data']['coupon']

			data = self.set_order.get_base_data(type)
			goods_pay = self.set_order.get_pay_amount(type, goods['goodsList'], goods['addGoodsList'])
			data['goodsList'] = goods_pay['goodsList']
			data['addGoodsList'] = goods_pay['addGoodsList']
			data['price'] = goods_pay['price']
			data['vip_price'] = goods_pay['vip_price']

			coupon_ret = self.set_order.validator_coupon(type, coupon_data, data['vip_price'], post_status)
			if coupon_ret:
				coupon_one = random.choice(coupon_ret)
				data['couponIds'] = [coupon_one['id']]
				data['price'] = data['price'] - coupon_one['amount']
				data['vip_price'] = data['vip_price'] - coupon_one['amount']

				# 获取联系方式
				picked = self.get_premise.picked_up_info()
				data['addressId'] = picked
				if type == 3:
					address_data = self.set_order.set_shop_wm()
					data['addressId'] = address_data['address_id']
					data['price'] = data['price'] + address_data['service_fee']
					data['vip_price'] = data['vip_price'] + address_data['service_fee']

				pay_ret = self.pay(data, 2)
				result_status = self.set_order.validator_pay(pay_ret, 2)
				if post_status == 1:
					data['cases_text'] = "使用优惠券下单"
					if not result_status:
						pay_ret['report_status'] = 500
				elif post_status == 2:
					data['cases_text'] = "使用当前时间不可用优惠券下单"
					pay_ret['report_status'] = 500
					if not result_status:
						pay_ret['report_status'] = 200
						pay_ret['code'] = 0
				elif post_status == 3:
					data['cases_text'] = "使用当前就餐方式可用优惠券下单"
					if not result_status:
						pay_ret['report_status'] = 500
				elif post_status == 4:
					data['cases_text'] = "使用当前就餐方式不可用优惠券下单"
					pay_ret['report_status'] = 500
					if not result_status:
						pay_ret['report_status'] = 200
						pay_ret['code'] = 0
				elif post_status == 2:
					data['cases_text'] = "使用金额达到使用条件优惠券下单"
					if not result_status:
						pay_ret['report_status'] = 500
				elif post_status == 2:
					data['cases_text'] = "使用金额未达到使用条件的优惠券下单"
					pay_ret['report_status'] = 500
					if not result_status:
						pay_ret['report_status'] = 200
						pay_ret['code'] = 0
				report = ""
				# 余额支付
				if result_status:
					time.sleep(1)
					cancel_status = self.cancel_order(pay_ret['data']['payment']['orderId'])
					if cancel_status:
						pay_ret = self.pay(data, 1)
						self.set_order.validator_pay(pay_ret, 1)
					else:
						report = "取消订单失败，orderId=" + str(pay_ret['data']['payment']['orderId'])
				result_status = {"key": [], "val": [], 'report': report}
				self.get_yaml_data.set_to_yaml(ret, data, pay_ret, ["订单", "下单"], result_status)
			else:
				pay_ret = {'data': {}, 'status': 200, 'code': 0, 'message': '', "request_time": 0, "traceid": 0}
				if post_status == 1:
					data['cases_text'] = "使用优惠券下单"
					pay_ret['report_status'] = 202
				elif post_status == 2:
					data['cases_text'] = "使用当前时间不可用优惠券下单"
					pay_ret['report_status'] = 202
				elif post_status == 3:
					data['cases_text'] = "使用当前就餐方式可用优惠券下单"
					pay_ret['report_status'] = 202
				elif post_status == 4:
					data['cases_text'] = "使用当前就餐方式不可用优惠券下单"
					pay_ret['report_status'] = 202
				elif post_status == 5:
					data['cases_text'] = "使用金额达到使用条件优惠券下单"
					pay_ret['report_status'] = 202
				elif post_status == 6:
					data['cases_text'] = "使用金额未达到使用条件的优惠券下单"
					pay_ret['report_status'] = 202
				report = "没有对应优惠券，跳过下单"
				result_status = {"key": [], "val": [], 'report': report}
				data['cases_text'] = self.get_type_code(type) + data['cases_text']
				self.get_yaml_data.set_to_yaml(ret, data, pay_ret, ["订单", "下单"], result_status)

		return result_status

	# 不支持就餐方式
	def shopping_way(self, type = 5):
		file_path = "/public/yaml/order/add.yaml"
		ret = self.get_config_data.get_data_post("postOrderUrl", file_path)
		data = self.set_order.get_base_data(type)
		goods_data = self.get_premise.get_goods(type, [1], 1)
		goods_params = []
		price = vip_price = box_price = 0
		for goods in goods_data:
			goods_post = self.set_order.add_goods_type_single(goods)
			goods_params.append(goods_post)
			price = price + goods_post['price'] * goods_post['number']
			vip_price = vip_price + goods_post['vipPrice'] * goods_post['number']
			box_price = box_price + goods_post['boxPrice'] * goods_post['number']
		goods_return = {"goods": goods_params, "price": price, "vip_price": vip_price, "box_price": box_price}
		# 加购
		add_goods = self.get_premise.get_add_goods(type)
		goods_pay = self.set_order.get_pay_amount(type, goods_return, add_goods)
		data['goodsList'] = goods_pay['goodsList']
		data['addGoodsList'] = goods_pay['addGoodsList']
		data['price'] = goods_pay['price']
		data['vip_price'] = goods_pay['vip_price']

		# 获取联系方式
		picked = 0
		if type == 4 or type == 5:
			picked = self.get_premise.picked_up_info()
		data['addressId'] = picked
		if type == 3:
			address_data = self.set_order.set_shop_wm()
			data['addressId'] = address_data['address_id']
			data['price'] = data['price'] + address_data['service_fee']
			data['vip_price'] = data['vip_price'] + address_data['service_fee']

		pay_ret = self.pay(data, 2)
		result_status = 200
		if pay_ret:
			result_status = self.set_order.validator_pay(pay_ret, 2)
		else:
			pay_ret = {'data': {}, 'status': 200, 'code': 0, 'message': '', "report_status": 202, "traceid": 0,
				"request_time": 0}
		data['cases_text'] = "购买不支持就餐方式的商品"
		if not result_status:
			pay_ret['report_status'] = 200
			pay_ret['code'] = 0
		report = ""
		# 余额支付
		if result_status:
			time.sleep(1)
			cancel_status = self.cancel_order(pay_ret['data']['payment']['orderId'])
			if cancel_status:
				pay_ret = self.pay(data, 1)
				self.set_order.validator_pay(pay_ret, 1)
			else:
				report = "取消订单失败，orderId=" + str(pay_ret['data']['payment']['orderId'])
		result_status = {"key": [], "val": [], 'report': report}
		data['cases_text'] = self.get_type_code(type) + data['cases_text']
		self.get_yaml_data.set_to_yaml(ret, data, pay_ret, ["订单", "下单"], result_status)

	# 营业时间内--库存充足情况下(成功)
	def stock_ample(self, type = 5):
		file_path = "/public/yaml/order/add.yaml"
		ret = self.get_config_data.get_data_post("postOrderUrl", file_path)
		for stock_data in [1, 2, 3]:  # 1小于起购 2等于/大于起购 3库存不足
			data = self.set_order.get_base_data(type)
			status = 0
			if stock_data == 3:
				status = 3
			goods_data = self.get_premise.get_goods(type, [1], status)
			goods_params = []
			price = vip_price = box_price = 0
			for goods in goods_data:
				if goods['min'] <= 1 and stock_data == 1:
					continue
				# 商品
				if stock_data == 1:
					goods['min'] = goods['min'] - 1
				goods_post = self.set_order.add_goods_type_single(goods)
				goods_params.append(goods_post)
				price = price + goods_post['price'] * goods_post['number']
				vip_price = vip_price + goods_post['vipPrice'] * goods_post['number']
				box_price = box_price + goods_post['boxPrice'] * goods_post['number']
			goods_return = {"goods": goods_params, "price": price, "vip_price": vip_price, "box_price": box_price}
			# 加购
			add_goods = self.get_premise.get_add_goods(type)
			goods_pay = self.set_order.get_pay_amount(type, goods_return, add_goods)
			data['goodsList'] = goods_pay['goodsList']
			data['addGoodsList'] = goods_pay['addGoodsList']
			data['price'] = goods_pay['price']
			data['vip_price'] = goods_pay['vip_price']

			# 获取联系方式
			picked = 0
			if type == 4 or type == 5:
				picked = self.get_premise.picked_up_info()
			data['addressId'] = picked
			if type == 3:
				address_data = self.set_order.set_shop_wm()
				data['addressId'] = address_data['address_id']
				data['price'] = data['price'] + address_data['service_fee']
				data['vip_price'] = data['vip_price'] + address_data['service_fee']

			pay_ret = self.pay(data, 2)
			result_status = self.set_order.validator_pay(pay_ret, 2)
			report = ""
			if stock_data == 1:
				data['cases_text'] = "购买数量小于最小起购数量"
				if not result_status:
					pay_ret['report_status'] = 200
					pay_ret['code'] = 0
			elif stock_data == 2:
				data['cases_text'] = "购买数量满足最小起购数量"
				if not result_status:
					pay_ret['report_status'] = 500
			elif stock_data == 3:
				data['cases_text'] = "购买库存不足的情况"
				if not result_status:
					pay_ret['report_status'] = 500
					pay_ret['code'] = 0
			# 余额支付
			if result_status:
				time.sleep(1)
				cancel_status = self.cancel_order(pay_ret['data']['payment']['orderId'])
				if cancel_status:
					pay_ret = self.pay(data, 1)
					self.set_order.validator_pay(pay_ret, 1)
				else:
					report = "取消订单失败，orderId=" + str(pay_ret['data']['payment']['orderId'])
			result_status = {"key": [], "val": [], 'report': report}
			data['cases_text'] = self.get_type_code(type) + data['cases_text']
			self.get_yaml_data.set_to_yaml(ret, data, pay_ret, ["订单", "下单"], result_status)

	# 非营业时间(成功)
	def business_time_out(self, type = 5):
		file_path = "/public/yaml/order/add.yaml"
		ret = self.get_config_data.get_data_post("postOrderUrl", file_path)

		shop_detail = self.get_premise.get_shop_detail()  # 获取店铺详情
		if shop_detail['data']['selfLiftRealStatus'] == 2 and shop_detail['data']['bookExpand'][
			'ztStatus'] == 1:  # 当前未营业,但是预定开启下预订单
			# 获取菜品
			send_time = self.get_premise.get_send_time(type)
			# [{'status': 1, 'time': 1557729600}, {'status': 2, 'time': 1558334400}]
			# status 1表示正常预定时间内  2表示非正常预定时间内
			# 获取预定时间满足条件的订单
			for send_time_data in send_time:
				goods = self.get_premise.get_order_goods_reserve(type, [1], 0)
				data = self.set_order.get_base_data(type)
				goods_pay = self.set_order.get_pay_amount(type, goods['goodsList'], goods['addGoodsList'])
				data['goodsList'] = goods_pay['goodsList']
				data['addGoodsList'] = goods_pay['addGoodsList']
				data['price'] = goods_pay['price']
				data['vip_price'] = goods_pay['vip_price']

				# 获取联系方式
				picked = 0
				if type == 4 or type == 5:
					picked = self.get_premise.picked_up_info()

				book_status = 1
				if send_time_data:
					book_status = 2
				data['addressId'] = picked
				if type == 3:
					address_data = self.set_order.set_shop_wm()
					data['addressId'] = address_data['address_id']
					data['price'] = data['price'] + address_data['service_fee']
					data['vip_price'] = data['vip_price'] + address_data['service_fee']

				data['book'] = book_status
				data['bookTime'] = send_time_data['time']
				data['addressId'] = self.get_premise.picked_up_info()
				pay_ret = self.pay(data, 2)
				result_status = self.set_order.validator_pay(pay_ret, 2)
				report = ""
				if send_time_data['status'] == 1:
					data['cases_text'] = "非营业时间内，预约开启，正常营业时间内，正常下预定单"
					if not result_status:
						pay_ret['report_status'] = 500
				elif send_time_data['status'] == 2:
					data['cases_text'] = "非营业时间内，预约开启，正常营业时间内，下非预定时间的订单"
					if result_status:
						pay_ret['report_status'] = 500
				# 余额支付
				if result_status:
					time.sleep(1)
					cancel_status = self.cancel_order(pay_ret['data']['payment']['orderId'])
					if cancel_status:
						pay_ret = self.pay(data, 1)
						self.set_order.validator_pay(pay_ret, 1)
					else:
						report = "取消订单失败，orderId=" + str(pay_ret['data']['payment']['orderId'])
				result_status = {"key": [], "val": [], 'report': report}
				data['cases_text'] = self.get_type_code(type) + data['cases_text']
				self.get_yaml_data.set_to_yaml(ret, data, pay_ret, ["订单", "下单"], result_status)

	# 是否营业

	# type_status 1自提外带 2不支持自提外带
	# sale_status 1可售  2不可售
	def get_goods(self, type = 1, goods_type = [1], type_status = 0, sale_status = 0):
		result = []
		# 获取菜品
		goods_list = self.get_premise.get_goods_list(type)

		if not goods_list:
			return False
		# 转化就餐方式
		if type == 1 or type == 4:
			shop_type = "dineIn"
		elif type == 2 or type == 5:
			shop_type = "takeAway"
		else:
			shop_type = "takeOut"
		# 获取菜品
		for goods in goods_list:
			if goods['type'] not in goods_type:
				continue
			if type_status == 2 and goods[shop_type] == 2:  # 不支持对应方式
				result.append(goods)
			elif sale_status == 2 and goods[shop_type] == 1 and goods['isSale'] == 2 \
					and int(goods['stock']) >= goods['min']:  # 不可售
				result.append(goods)
			# elif goods[shop_type] == 1 and goods['isSale'] == 1 and int(goods['stock']) < goods['min']:  # 库存不足
			# 	result.append(goods)
			elif goods[shop_type] == 1 and goods['isSale'] == 1 and int(goods['stock']) >= goods['min']:  # 充足条件
				result.append(goods)
		return result

	def get_type_code(self, type):
		if type == 1:
			return "【堂食】"
		if type == 2:
			return "【外带】"
		if type == 3:
			return "【外卖】"
		if type == 4:
			return "【自提堂食】"
		if type == 5:
			return "【自提外带】"

	# 取消订单
	def cancel_order(self, orderId):
		file_path = "/public/yaml/order/cancel.yaml"
		ret = self.get_config_data.get_data_post("closeOrder", file_path)
		url = ret['url']
		header = ret['header']
		data = {"orderId": orderId}
		params = self.send_post.send_post(url, data, header)
		if params['status'] != 200:
			return False

		return True

	# 新增订单  pay_type 1全额余额支付  2微信支付
	def pay(self, data, pay_type = 2):
		user = self.get_premise.get_user_info()  # 获取用户信息
		if not user:
			return False
		# 验证菜品
		check_status = self.set_order.check_goods(data)
		if not check_status:
			return False
		discount = int(user['data']['discount']) / 10000

		if user['data']['vipId']:
			pay_amount = int(data['vip_price'])
		else:
			pay_amount = int(data['price'])
		pay_amount = int(pay_amount * discount)
		if pay_type == 2:
			data['payAmount'] = pay_amount
			data['balance'] = 0
		else:
			data['balance'] = pay_amount
			data['payAmount'] = 0

		params_post = self.get_config_data.get_conf("postOrderUrl")
		params = self.send_post.send_post(params_post['url'], data, params_post['header'])
		return params


if __name__ == '__main__':
	run = OrderData()
	ret = run.order_package(3)
	print(ret)
	exit()
