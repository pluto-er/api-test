# coding:utf-8
import sys
import os
import time
import random
import json
import datetime

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from helper.get_yaml import GetYaml
from helper.get_html import GetHtml
from helper.request_post import SendPost
from helper.validator import ValidatorHelper
from helper.get_config import GetDataConfig
from helper.get_geo import GetGeo

from data.goodsdata import GoodsData
from data.userdata import UserData
from data.shopdata import ShopData
from data.addressdata import AddressData
from datetime import datetime


class OrderData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()
		self.get_geo = GetGeo()
		self.goods = GoodsData()
		self.user = UserData()
		self.shop = ShopData()
		self.address = AddressData()

	# 订单列表
	def list(self, model, post_data = None):
		file_path = "/public/yaml/order/list.yaml"
		ret = self.get_config_data.get_data_post("getOrderList", file_path)
		url = ret['url']
		header = ret['header']
		if not post_data:
			post_data = ret['expect']['retData']

		for data in post_data:
			total = 0
			cases_text = data['cases_text']
			page_text = {1: "", 0: "第0页", 100: "最后一页", 101: "大于最后一页"}
			for page_post in [1, 0, 100, 101]:
				# 请求api获取结果
				data['page'] = page_post
				page_data = self.validator.set_page(data, total)
				data['page'] = page_data['page']
				page_size = page_data['page_size']

				params = self.send_post.send_post(url, data, header)
				result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
				if result_status == "fail":
					continue

				# 特殊·断言
				report = ""
				total = params['data']['count']
				report += self.validator.page(page_size, params['data']['count'], params['data']['list'], data)

				for request_data in params['data']['list']:
					if data['status'] and request_data['status'] not in data['status']:
						params['report_status'] = 202
						report += "用户状态错误，status=" + str(request_data['status']) + "<br/>"
					if request_data['payTime'] + 86400 * 3 < int(time.time()) and request_data['status'] not in [9, 10]:
						params['report_status'] = 202
						report += "3天过去未完成数据，orderno=" + request_data['orderno'] + "<br/>"
					if request_data['updateTime'] + 3600 < int(time.time()) and request_data['type'] == 3 and \
							request_data[
								'dispatchType'] not in [6, 7, 8] and request_data['deliveryType'] not in [1, 2]:
						params['report_status'] = 202
						report += "外卖订单一个小时内未发生状态改变，orderno=" + str(request_data['orderno']) + "<br/>"
				result_status['report'] = report
				data['cases_text'] = page_text[page_post] + cases_text
				self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 订单不同状态的计数统计
	def count(self, model):
		file_path = "/public/yaml/order/count.yaml"
		ret = self.get_config_data.get_data_post("getOrderCount", file_path)
		url = ret['url']
		header = ret['header']
		data = []

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == "fail":
			return 500

		# 获取未评论数
		data = {'status': [8], 'page': 1, 'size': 10, 'refundType': [1, 2]}
		url = ret['host'] + "/order/list"
		# 获取订单
		ret_list_data = self.list(model, [{"status": [9], "page": 1, "size": 10, "refundType": []}])

		report = ""
		if int(ret_list_data['data']['count']) != int(params['data']['waitCommentCount']):
			params['report_status'] = 202
			report += "数量错误，list_count=" + str(ret_list_data['data']['count']) + ";总计count=" + str(
					params['data']['waitCommentCount']) + "<br/>"

		result_status['report'] = report
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 订单详情
	def detail(self, model):
		file_path = "/public/yaml/order/detail.yaml"
		ret = self.get_config_data.get_data_post("orderDetail", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		for data in post_data:
			for type in [1, 2, 3, 4, 5, 8, 9, 10]:
				if type == 1:
					data['cases_text'] = "待付款订单详情"
				elif type == 2:
					data['cases_text'] = "待配送订单详情"
				elif type == 3:
					data['cases_text'] = "配送中订单详情"
				elif type == 4:
					data['cases_text'] = "备餐中订单详情"
				elif type == 5:
					data['cases_text'] = "制作中订单详情"
				elif type == 8:
					data['cases_text'] = "待评价订单详情"
				elif type == 9:
					data['cases_text'] = "已完成订单详情"
				elif type == 10:
					data['cases_text'] = "已取消订单详情"
				params_post = self.get_config_data.get_conf("getOrderList")
				order = self.send_post.send_post(params_post['url'], {"status": [type]}, params_post['header'])
				if not order['data']['list']:
					result_status = {"key": [], "val": [], 'report': "没有订单，type=" + str(type)}
					self.get_yaml_data.set_to_yaml(ret, data, order, model, result_status)
					continue
				choice_order = random.choice(order['data']['list'])
				data['id'] = choice_order['id']
				# 请求api获取结果
				params = self.send_post.send_post(url, data, header)
				result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
				if result_status == "fail":
					continue

				self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 新增订单
	def add(self, model):
		file_path = "/public/yaml/order/add.yaml"
		ret = self.get_config_data.get_data_post("postOrderUrl", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		for data in post_data:  # 循环就餐类型
			shop_detail = self.shop.detail(model)
			if shop_detail == 500 or not shop_detail['data']:
				continue
			# 判断当前就餐方式是否支持预订单
			shop_reserve = self.decide_reserve(data['type'], shop_detail['data']['bookExpand'])
			# 获取商品 多规格
			goods_type_list = [[1], [2], [3], [1, 2], [2, 3], [1, 3], [1, 2, 3]]
			# 注释说明  当goods_type_list，spec_status_list，coupon_status_list 当前是错误的后一个一定是正确，
			# 当前是正确的后一个可能为正确、错误
			goods_sale_list = [1, 2, 4]  # 1正常可售 2时间不可售 3下架(列表不返回可以不做要求) 4库存/限量
			spec_status_list = [1, 2]  # 1正常 2必须加购未加购
			coupon_status_list = [1, 3]  # 1正常可用优惠券 2无优惠券 3不可用的优惠券 4菜品券(我是老用户不可用菜品券)(未有菜品券，先不测试)
			for shop_reserve_data in shop_reserve:  # 预定、非预定
				for goods_type in goods_type_list:  # 循环菜品类型  单品、多规格、套餐及组合
					for sale_status in goods_sale_list:
						for spec_status in spec_status_list:
							for coupon_status in coupon_status_list:
								if sale_status != 1 and spec_status != 1:
									continue
								if (sale_status != 1 or spec_status != 1) and coupon_status != 1:
									continue
								time.sleep(3)
								try:
									if data['type'] in [1, 2]:  # 堂食
										res = self.add_order_ts(data['type'], shop_reserve_data, goods_type,
																sale_status, spec_status)
										if res == 500:
											self.set_to_yaml(ret, data, model, "没有菜品,type=" + str(data['type']))
											continue
									if data['type'] == 3:  # 外卖
										res = self.add_order_wm(data['type'], shop_reserve_data, goods_type,
																sale_status, spec_status)
										if res == 500:
											self.set_to_yaml(ret, data, model, "没有菜品,type=" + str(data['type']))
											continue
										data['addressId'] = res['addressId']
										data['book'] = shop_reserve_data
										data['bookTime'] = res['bookTime']
									if data['type'] in [4, 5]:  # 自提
										res = self.add_order_wd(data['type'], shop_reserve_data, goods_type,
																sale_status, spec_status)
										if res == 500:
											self.set_to_yaml(ret, data, model, "没有菜品,type=" + str(data['type']))
											continue
										data['addressId'] = res['addressId']
										data['book'] = shop_reserve_data
										data['bookTime'] = res['bookTime']

									# 验证菜品
									check_status = self.check_goods(res)
									# print(check_status)
									# exit()
									if check_status == 500:
										self.set_to_yaml(ret, data, model, "验证菜品失败,type=" + str(data['type']))
										continue

									# 获取用户等级和余额
									user = self.user.info(model)
									if not user:
										continue
									discount = int(user['discount']) / 10000
									balance = user['balance']

									if user['vipId']:
										pay_amount = int(res['vip_price'])
									else:
										pay_amount = int(res['price'])

									# 优惠券
									data['couponIds'] = []
									coupon_data = self.coupon_list(pay_amount, data['type'], coupon_status)
									if coupon_data:
										pay_amount = pay_amount - int(coupon_data['amount'])
										data['couponIds'] = [coupon_data['id']]
									pay_amount = abs(int(pay_amount * discount))
									data['balance'] = random.randint(0, pay_amount)
									if balance < data['balance']:
										data['balance'] = balance
									data['payAmount'] = pay_amount - data['balance']
									data['addGoodsList'] = res['addGoodsList']
									data['goodsList'] = res['goodsList']
									# 微信支付
									# print(
									# 		"sale_status=" + str(sale_status) + ";spec_status=" + str(
									# 				spec_status) + ";coupon_status=" + str(coupon_status))
									# print(data)
									ret['expect']['result'] = {'data': {'payment': {'appId': 'wxd9a28df0646534d8',
										'timeStamp': '1528272139', 'nonceStr': 'ZqVLm8Pat11R1lES',
										'package': 'prepay_id=wx0616310921997445847a6bb82103985001', 'signType': 'MD5',
										'paySign': 'CD4DF19AE59427DFE83517F0A71CC9DA', 'orderId': 12345,
										'orderno': '155641426764551068878', 'payAmount': 10240,
										'prepayId': 'wx280917482887322d8d7918c11135339134'}, 'type': 1},
										'status': 200, 'code': 0, 'message': '', 'serverTime': 1554209408.009201}

									params = self.send_post.send_post(url, data, header)

									# print(params)
									if int(sale_status) == 2 and params['status'] == 200 and params['code'] == 0:
										result_status = {"key": [], "val": [], 'report': "菜品在非可售时间内下单，下单成功"}
										params['status'] = 500
										params['message'] = "购物车内有菜品在非可售时间内，但是下单成功"
										self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)
										continue
									if int(sale_status) == 4 and params['status'] == 200 and params['code'] == 0:
										result_status = {"key": [], "val": [], 'report': "库存不足，下单成功"}
										params['status'] = 500
										params['message'] = "购物车内有菜品库存不足，但是下单成功"
										self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)
										continue
									if int(spec_status) == 2 and params['status'] == 200 and params['code'] == 2:
										result_status = {"key": [], "val": [],
											'report': params['message'] + "有必选加购产品，但是未选择 "}
										params['code'] = 0
										self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)
										continue
									if int(coupon_status) == 3 and params['status'] == 200 and params['code'] == 2:
										result_status = {"key": [], "val": [], 'report': "优惠券不能使用，消费金额未达到"}
										params['code'] = 0
										self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)
										continue
									if int(params['code']) == 15005:
										result_status = {"key": [], "val": [], 'report': params['message']}
										params['code'] = 0
										params['report_status'] = 202
										self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)
										continue
									if int(params['code']) == 1:
										result_status = {"key": [], "val": [], 'report': "库存不足"}
										params['code'] = 0
										params['message'] = "库存不足"
										params['report_status'] = 200
										self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)
										continue

									result_status = self.validator.validate_status(ret, params, model, data)
									if result_status == "fail":
										continue

									# 取消订单
									cancel_status = self.cancel_order(params['data']['payment']['orderId'])
									if cancel_status == 500:
										continue

									# 再次使用余额支付
									if balance < pay_amount:
										result = 500
										params['message'] = "余额不足"
										self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)
										continue

									data['balance'] = pay_amount
									data['payAmount'] = 0
									data['payType'] = 1
									data['goods_type'] = goods_type
									ret['expect']['result'] = {'data': {'payment': {'orderId': 12345}, 'type': 1},
										'status': 200, 'code': 0, 'message': '', 'serverTime': 1554209408.009201}
									params = self.send_post.send_post(url, data, header)
									result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
									if result_status == "fail":
										continue

									self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)
								except BaseException as e:
									result_status = {"key": [], "val": [], 'report': str(e)}
									params = {"report_status": 202, "request_time": 0, "traceid": "", "status": 200,
										"code": 0, "message": str(e)}
									self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 处理堂食
	# shop_reserve_data 预定 goods_type 菜品类型  sale_status 售卖情况   spec_status 加购
	def add_order_ts(self, order_type, shop_reserve_data, goods_type, sale_status, spec_status):
		# 获取商品
		goods_list = self.get_goods_shopping(order_type, shop_reserve_data, goods_type, sale_status)
		if goods_list == 500:
			return 500
		if not goods_list['goods_list']:
			return 500
		# 获取加购
		goods_add = self.get_goods_add_shopping(order_type, spec_status)
		result = {
			'goodsList': goods_list['goods_list'],
			'addGoodsList': goods_add['goods_add'],
			'price': goods_list['price'] + goods_add['price'],
			'vip_price': goods_list['vip_price'] + goods_add['vip_price']
			}

		return result

	# 处理外卖
	def add_order_wm(self, order_type, shop_reserve_data, goods_type, sale_status, spec_status):
		# 获取商品
		goods_list = self.get_goods_shopping(order_type, shop_reserve_data, goods_type, sale_status)

		if goods_list == 500 or not goods_list['goods_list']:
			return 500

		book_time = goods_list['bookTime']
		# 店铺详情
		shop_detail = self.shop.detail(['订单', '下单'])

		# 获取地址列表
		file_path = "/public/yaml/user/address_list.yaml"
		ret = self.get_config_data.get_data_post("getUserAddress", file_path)
		url = ret['url']
		header = ret['header']
		data = {"lat": shop_detail['data']['lat'], "lat": shop_detail['data']['lon']}
		params = self.send_post.send_post(url, data, header)
		# 选取满足条件的地址
		choice_address = []
		for address_post in params['data']:
			if address_post['usual'] == 1:
				choice_address.append(address_post)
		if not choice_address:
			return 500
		address_data = random.choice(choice_address)

		price_url = ret['host'] + "/shop/shop/get-distribution-price"
		price_data = {"time": book_time, "lat": address_data['lat'], "lon": address_data['lon']}
		price_params = self.send_post.send_post(price_url, price_data, header)
		service_fee = price_params['data']['totalPrice']
		start_price = price_params['data']['startingPrice']

		# 判断是否满足最低起送价
		if start_price > goods_list['price']:
			num = int(start_price / goods_list['price']) + random.randint(1, 3)
			goods_list = self.get_goods_shopping(order_type, shop_reserve_data, goods_type, sale_status)

		# 获取加购
		goods_add = self.get_goods_add_shopping(order_type, spec_status)
		result = {
			'bookTime': book_time,
			'goodsList': goods_list['goods_list'],
			'addGoodsList': goods_add['goods_add'],
			'addressId': address_data['id'],
			'price': goods_list['price'] + goods_add['price'] + service_fee,
			'vip_price': goods_list['vip_price'] + goods_add['vip_price'] + service_fee
			}

		return result

	# 处理自提
	def add_order_wd(self, order_type, shop_reserve_data, goods_type, sale_status, spec_status):
		# 获取商品
		goods_list = self.get_goods_shopping(order_type, shop_reserve_data, goods_type, sale_status)
		if goods_list == 500 or not goods_list['goods_list']:
			return 500

		book_time = goods_list['bookTime']

		# 获取加购
		goods_add = self.get_goods_add_shopping(order_type, spec_status)
		# 获取联系人电话
		picked = self.user.picked_up_info()
		if not picked['data']:
			return 500
		result = {
			'bookTime': book_time,
			'goodsList': goods_list['goods_list'],
			'addGoodsList': goods_add['goods_add'],
			'addressId': picked['data']['id'],
			'price': goods_list['price'] + goods_add['price'],
			'vip_price': goods_list['vip_price'] + goods_add['vip_price']
			}

		return result

	# 处理单品
	def add_goods_type_single(self, goods_data, num = 1):
		goods_list = {}
		goods_list['attributes'] = []
		goods_list['goodsCouponId'] = 0
		goods_list['id'] = goods_data['gid']
		goods_list['number'] = goods_data['min'] * num
		goods_list['type'] = goods_data['type']

		if goods_data['vipPrice'] == 0:
			goods_list['vipPrice'] = goods_data['price']
		else:
			goods_list['vipPrice'] = goods_data['vipPrice']
		goods_list['price'] = goods_data['price']
		goods_list['boxPrice'] = goods_data['boxPrice']

		return goods_list

	# 处理多规格
	def add_goods_type_space(self, goods_data, num = 1):
		goods_list = {'goodsCouponId': 0, 'type': goods_data['type']}
		# 获取规格
		spec_list = goods_data['detail']['spec']['list']

		goods_detail_list = spec_list[random.randint(0, len(spec_list) - 1)]

		goods_list['id'] = goods_detail_list['gid']
		goods_list['price'] = goods_detail_list['price']
		goods_list['boxPrice'] = goods_detail_list['boxPrice']
		goods_list['number'] = goods_data['detail']['info']['min'] * num

		if goods_detail_list['vipPrice'] == 0:
			goods_list['vipPrice'] = goods_detail_list['price']
		else:
			goods_list['vipPrice'] = goods_detail_list['vipPrice']

		# 获取属性
		if goods_data['detail']['property']:
			property_list = goods_data['detail']['property']
			goods_property_list = property_list[random.randint(0, len(property_list) - 1)]
			goods_property_data = goods_property_list['list'][random.randint(0, len(goods_property_list['list']) - 1)]

			attributes = {'id': goods_property_list['id'],
				'valueId': goods_property_data['id']}
			goods_list['attributes'] = []
			goods_list['attributes'].append(attributes)

		return goods_list

	# 处理套餐
	def add_goods_type_package(self, goods_data, num = 1):
		goods_list = {'id': goods_data['gid'], 'number': goods_data['min'] * num, 'type': goods_data['type'],
			'goodsList': []}
		price = vip_price = box_price = 0
		# 必选菜品
		for goods_check_list_data in goods_data['detail']['package']['list']:
			for goods in goods_check_list_data['parts']:
				goods_data_list = {'groupId': goods_check_list_data['id'], 'attributes': [], 'id': goods['gid'],
					'type': goods['type'], 'number': goods['min'], 'name': goods['name']}

				if goods['packageVipPrice'] == 0:
					goods_data_list['vipPrice'] = goods['packagePrice']
				else:
					goods_data_list['vipPrice'] = goods['packageVipPrice']

				goods_data_list['price'] = goods['packagePrice']
				goods_data_list['boxPrice'] = goods['boxPrice']
				# 获取规格
				if goods['type'] == 2:
					goods_spec = goods_data['detail']['property'][str(goods['gid'])]
					goods_property_list = goods_spec[random.randint(0, len(goods_spec) - 1)]
					goods_property_data = goods_property_list['list'][
						random.randint(0, len(goods_property_list['list']) - 1)]

					attributes = {'id': goods_property_list['id'],
						'valueId': goods_property_data['id']}

					goods_data_list['attributes'].append(attributes)
				goods_list['goodsList'].append(goods_data_list)

				price = price + goods_data_list['price'] * goods_data_list['number']
				vip_price = vip_price + goods_data_list['vipPrice'] * goods_data_list['number']
				box_price = box_price + goods_data_list['boxPrice'] * goods_data_list['number']
				if goods_check_list_data['multi'] == 1:
					break
		goods_list['price'] = price
		goods_list['vipPrice'] = vip_price
		goods_list['boxPrice'] = box_price
		return goods_list

	# 加购
	def goods_add(self, goodsAdd, spec_status):
		# 加购必选
		add_goods_result = []
		if spec_status == 1:
			for goods_add_data in goodsAdd['data']['required']:
				if goods_add_data['vipPrice'] == 0:
					goods_add_data['vipPrice'] = goods_add_data['price']
				add_goods_list = {
					"id": goods_add_data['id'],
					"number": goods_add_data['min'],
					"type": goods_add_data['type'],
					"vipPrice": goods_add_data['vipPrice'],
					"price": goods_add_data['price'],
					"boxPrice": goods_add_data['boxPrice'],
					'goodsCouponId': 0,
					'attributes': []
					}
				add_goods_result.append(add_goods_list)

		for goods_add_data in goodsAdd['data']['option']:
			if goods_add_data['vipPrice'] == 0:
				goods_add_data['vipPrice'] = goods_add_data['price']
			add_goods_list = {
				"id": goods_add_data['id'],
				"number": goods_add_data['min'],
				"type": goods_add_data['type'],
				"vipPrice": goods_add_data['vipPrice'],
				"price": goods_add_data['price'],
				"boxPrice": goods_add_data['boxPrice'],
				'goodsCouponId': 0,
				'attributes': []
				}
			add_goods_result.append(add_goods_list)

		return add_goods_result

	# 获取优惠券
	def coupon_list(self, money, order_type, coupon_status):
		# 订单类型
		result_data = []
		if coupon_status == 2:
			return result_data
		# 加载couponData
		from data.coupondata import CouponData
		self.coupon = CouponData()
		data = self.coupon.coupon_able_list(['订单', '优惠券'])
		if "coupon" not in data:
			return []
		result = []
		# 优惠券
		if data['coupon']:
			for coupon_data in data['coupon']:
				if coupon_data['condition'] > money and coupon_status == 1:
					continue
				scenarios_list = coupon_data['scenarios'].split(",")
				is_used = 1
				if str(order_type) in scenarios_list and coupon_status == 1:
					if coupon_data['usetime'] == '[]':
						is_used = 1
					else:
						is_used = 2
						use_time = json.loads(coupon_data['usetime'])
						for week_time in use_time:
							now_week = datetime.today().isoweekday()
							this_time = time.strftime("%H:%M")
							if str(now_week) not in week_time['week']:
								continue

							for now_time in week_time['time']:
								star_time = self.get_time(now_time['start'])
								end_time = self.get_time(now_time['end'])
								this_time = self.get_time(this_time)
								if star_time <= this_time <= end_time:
									is_used = 1

				if is_used == 2:
					continue
				result.append(coupon_data)
			if result:
				result_data = random.choice(result)
		return result_data

	# 获取时间
	def get_time(self, this_time):
		if this_time == "00:00":
			return 0
		star = str('1970-01-01 ' + this_time + ':00')
		timeArray = time.strptime(star, "%Y-%m-%d %H:%M:%S")
		timeStamp = int(time.mktime(timeArray))
		return timeStamp

	# 验证菜品
	def check_goods(self, res):
		# 验证菜品
		goods_list_number = []
		for goods_number_data in res['goodsList']:
			goods_number = {'gid': goods_number_data['id'], 'num': goods_number_data['number']}
			goods_list_number.append(goods_number)

		for goods_number_data in res['addGoodsList']:
			goods_number = {'gid': goods_number_data['id'], 'num': goods_number_data['number']}
			goods_list_number.append(goods_number)

		file_path = "/public/yaml/goods/check.yaml"
		check = self.get_config_data.get_data_post("checkGoodsStatusList", file_path)
		check_url = check['url']
		header = check['header']
		check_data = {'gids': goods_list_number}
		params_data = self.send_post.send_post(check_url, check_data, header)
		result_status = self.validator.validate_status(check, params_data, ['订单', '下单'], check_data)  # 判断status
		if result_status == "fail":
			return 500

		return 200

	# 取消订单
	def cancel_order(self, orderId):
		file_path = "/public/yaml/order/cancel.yaml"
		ret = self.get_config_data.get_data_post("closeOrder", file_path)
		url = ret['url']
		header = ret['header']
		data = {"orderId": orderId}
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, ['订单', '取消订单'], data)  # 判断status
		if result_status == "fail":
			return 500

		return 200

	# 获取购物车  前三个条件必判断
	def get_goods_shopping(self, order_type, shop_reserve_data, goods_type, sale_status, num = 1):
		# 获取对应商品
		send_time = self.get_send_time(order_type, shop_reserve_data)
		now = 0
		if send_time:
			now = int(time.mktime(time.strptime(send_time, "%Y-%m-%d %H:%M:%S")))
		goods = self.goods.get_shopping(order_type, goods_type, shop_reserve_data, send_time)
		if not goods:
			return 500
		# 开始组装数据
		goods_list_data = []
		price = vip_price = box_price = 0
		for goods_data in goods:
			if sale_status == 2:  # 不可售
				if goods_data['isSale'] == 1:
					continue
			elif sale_status == 3:  # 库存不足
				if int(goods_data['stock']) >= int(goods_data['min']):
					continue
			else:
				if goods_data['isSale'] == 2:
					continue
				if int(goods_data['stock']) < int(goods_data['min']):  # 去除库存不足情况
					continue
			if goods_data['type'] == 1:
				goods_list = self.add_goods_type_single(goods_data, num)
			elif goods_data['type'] == 2:
				goods_list = self.add_goods_type_space(goods_data, num)
			else:
				goods_list = self.add_goods_type_package(goods_data, num)
			goods_list_data.append(goods_list)
			price = price + goods_list['price'] * goods_list['number']
			vip_price = vip_price + goods_list['vipPrice'] * goods_list['number']
			box_price = box_price + goods_list['boxPrice'] * goods_list['number']
		if order_type in [2, 3, 5]:
			price = price + box_price
			vip_price = vip_price + box_price

		return {'goods_list': goods_list_data, 'price': price, 'vip_price': vip_price, 'book': shop_reserve_data,
			'bookTime': now}

	# 获取加购-购物车  spec_status为1正常  2表示必须加购却没加购
	def get_goods_add_shopping(self, order_type, spec_status):
		# 获取加购商品
		goods_add = self.goods.get_addition(order_type)
		goods_add_data = self.goods_add(goods_add, spec_status)
		price = vip_price = box_price = 0
		for add_price in goods_add_data:
			price = price + add_price['price'] * add_price['number']
			vip_price = vip_price + add_price['vipPrice'] * add_price['number']
			box_price = box_price + add_price['boxPrice'] * add_price['number']
		if order_type in [2, 3, 5]:
			price = price + box_price
			vip_price = vip_price + box_price
		return {'goods_add': goods_add_data, 'price': price, 'vip_price': vip_price}

	# 判断是否营业
	def decide_shop(self, shop_type, shop_detail):
		is_status = 2
		if str(shop_type) in shop_detail:
			now_week = datetime.today().isoweekday()
			now_time = time.strftime("%H:%M")
			for data in shop_detail[str(shop_type)]:
				shop_week = data['timeType'].strip(',').split(',')
				if str(now_week) not in shop_week:
					continue
				for data_time in data['timePeriod']:
					if data_time['start'] <= now_time <= data_time['end']:
						is_status = 1
		return is_status

	# 判断是否预定
	def decide_reserve(self, shop_type, book_expand):
		reserve_status = [1]  # 1表示不预定，2表示预定
		if shop_type in [1, 2]:
			return reserve_status
		if shop_type == 3:
			if book_expand['wmStatus'] == 1:
				reserve_status.append(2)
		if shop_type in [4, 5]:
			if book_expand['ztStatus'] == 1:
				reserve_status.append(2)

		return reserve_status

	# 获取预定时间  如果非预定时间为0
	def get_send_time(self, shop_type, shop_reserve_data):
		# 获取文件请求数据
		if shop_reserve_data == 1:
			return 0
		file_path = "/public/yaml/shop/get_send_time.yaml"
		ret = self.get_config_data.get_data_post("getStoreDistributionList", file_path)
		url = ret['url']
		header = ret['header']
		data = {'type': shop_type}

		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, ['订单', '预约时间'], data)  # 判断status
		if result_status == 'fail':
			return 500
		if not params['data']:
			return 0
		ret_data = random.choice(params['data'])
		send_data = ret_data['date'] + " " + random.choice(ret_data['timeList']) + ":00"

		return send_data

	# 写入空订单
	def set_to_yaml(self, ret, data, model, report):
		result_status = {"key": [], "val": [], 'report': report}
		params = {"report_status": 202, "request_time": 0, "traceid": "", "status": 200, "code": 0, "message": ""}
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)


if __name__ == '__main__':
	run = OrderData()
	ret = run.add()
	print(ret)
	exit()
