# coding:utf-8
import sys
import os
import random
import datetime
import time
import json
import datetime
import time

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from helper.request_post import SendPost
from helper.get_config import GetDataConfig
from helper.validator import ValidatorHelper
from helper.get_yaml import GetYaml


class SetOrder:

	def __init__(self):
		self.send_post = SendPost()
		self.get_config_data = GetDataConfig()
		self.validator = ValidatorHelper()
		self.get_yaml_data = GetYaml()

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

		header = self.get_config_data.get_conf("getGoodsDetailUrl")
		goods_spec_data = self.send_post.send_post(header['host'] + header['uri'], {"glid": goods_data['id']},
												   header['header'])
		goods_data['detail'] = goods_spec_data['data']

		spec_list = goods_data['detail']['spec']['list']

		goods_detail_list = random.choice(spec_list)

		goods_list['number'] = goods_data['detail']['info']['min'] * num
		goods_list['id'] = goods_detail_list['gid']
		goods_list['price'] = goods_detail_list['price']
		goods_list['boxPrice'] = goods_detail_list['boxPrice']

		if goods_detail_list['vipPrice'] == 0:
			goods_list['vipPrice'] = goods_detail_list['price']
		else:
			goods_list['vipPrice'] = goods_detail_list['vipPrice']

		# 获取属性
		if goods_data['detail']['property']:
			property_list = goods_data['detail']['property']
			goods_property_list = random.choice(property_list)
			goods_property_data = random.choice(goods_property_list['list'])

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
		header = self.get_config_data.get_conf("getPackageDetailUrl")
		goods_spec_data = self.send_post.send_post(header['url'], {"glid": goods_data['id']}, header['header'])
		goods_data['detail'] = goods_spec_data['data']
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
					goods_property_list = random.choice(goods_spec)
					goods_property_data = random.choice(goods_property_list['list'])

					attributes = {'id': goods_property_list['id'],
						'valueId': goods_property_data['id']}

					goods_data_list['attributes'].append(attributes)
				goods_list['goodsList'].append(goods_data_list)

				price = price + goods_data_list['price'] * goods_data_list['number']
				vip_price = vip_price + goods_data_list['vipPrice'] * goods_data_list['number']
				box_price = box_price + goods_data_list['boxPrice'] * goods_data_list['number']
				if goods_check_list_data['multi'] == 1:
					break
		package_coupon = self.validator_package_coupon(type, goods_data['detail']['package'], price, vip_price,
													   box_price)
		goods_list['price'] = package_coupon['price']
		goods_list['vipPrice'] = package_coupon['vip_price']
		goods_list['boxPrice'] = box_price
		return goods_list

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
		header = self.get_config_data.get_conf("checkGoodsStatusList")
		params = self.send_post.send_post(header['host'] + header['uri'], {'gids': goods_list_number}, header['header'])
		# if params['status'] != 200:
		# 	return False

		return params

	# 设置请求数据
	def get_base_data(self, type):
		data = {
			"goodsList": [],
			"addGoodsList": [],
			"couponIds": [],
			"balance": 0,
			"payAmount": 0,
			"type": type,
			"payType": 2,
			"payMethod": 2,
			"remark": "",
			"book": 1,
			"bookTime": 0,
			"tableId": 90,
			"dinnersNumber": 0,
			"addressId": 0,
			"price": 0,
			"vip_price": 0,
			"uniqueCode": "680c93cb-5989-1b5f-0e86-aad051bc7771"
			}

		return data

	# 校验支付结果值
	def validator_pay(self, params, type = 2):
		if not params:
			return False
		if type == 2:
			expect = {'data': {'payment': {'appId': 'wxd9a28df0646534d8',
				'timeStamp': '1528272139', 'nonceStr': 'ZqVLm8Pat11R1lES',
				'package': 'prepay_id=wx0616310921997445847a6bb82103985001', 'signType': 'MD5',
				'paySign': 'CD4DF19AE59427DFE83517F0A71CC9DA', 'orderId': 12345,
				'orderno': '155641426764551068878', 'payAmount': 10240,
				'prepayId': 'wx280917482887322d8d7918c11135339134'}, 'type': 1},
				'status': 200, 'code': 0, 'message': '', 'serverTime': 1554209408.009201}
		else:
			expect = {'data': {'payment': {'orderId': 12345}, 'type': 1},
				'status': 200, 'code': 0, 'message': '', 'serverTime': 1554209408.009201}

		if int(params['code']) == 0 and int(params['status'] == 200):
			ret = self.validator.get_round_status(expect['data'], params['data'], 0, [], [])
			if ret['key'] or ret['val']:
				return False
			else:
				return True
		else:
			return False

	# 计算价格
	def get_pay_amount(self, type, goods, add_goods):
		data = {}
		data['goodsList'] = goods['goods']
		data['addGoodsList'] = add_goods['add_goods']

		data['price'] = goods['price'] + add_goods['add_goods_price']
		data['vip_price'] = goods['vip_price'] + add_goods['add_goods_vip_price']

		if type in [2, 3, 5]:
			data['price'] = data['price'] + goods['box_price'] + add_goods['add_goods_box_price']
			data['vip_price'] = data['vip_price'] + goods['box_price'] + add_goods['add_goods_box_price']
		return data

	# 判断优惠券条件
	# coupon_status 1正常 2不在使用时间内 3就餐方式满足  4 就餐方式不满足 5金额满足 6金额不满足
	def validator_coupon(self, order_type, data, money, coupon_status, book_time = 0):
		if order_type == 4:
			order_type = 1
		elif order_type == 5:
			order_type = 2
		coupon = []
		for coupon_data in data:
			if coupon_status == 6 and coupon_data['condition'] < money:
				continue

			if coupon_data['condition'] > money and coupon_status != 6:
				continue
			# 就餐方式
			scenarios_list = coupon_data['scenarios'].split(",")
			if str(order_type) in scenarios_list and coupon_status == 4:
				continue
			if str(order_type) not in scenarios_list and coupon_status != 4:
				continue
			# 时间使用情况
			if coupon_data['usetime'] == '[]' and coupon_status == 2:
				continue
			if coupon_data['usetime'] == '[]' and coupon_status == 1:
				coupon.append(coupon_data)
				continue
			if coupon_data['usetime']:
				use_time = json.loads(coupon_data['usetime'])
				for week_time in use_time:
					if book_time == 0:
						book_time = None
					time_str = time.localtime(book_time)
					now_week = time.strftime("%w", time_str)
					this_time = time.strftime("%H:%M", time_str)
					if str(now_week) not in week_time['week'] and coupon_status == 2:
						coupon.append(coupon_data)
						break
					if str(now_week) not in week_time['week'] and coupon_status != 2:
						continue

					for now_time in week_time['time']:
						if (now_time['start'] <= this_time <= now_time['end']) and coupon_status == 2:
							continue
						if (now_time['start'] <= this_time <= now_time['end']) and coupon_status != 2:
							coupon.append(coupon_data)

		return coupon

	# 配送相关
	def set_shop_wm(self):
		# 店铺详情
		params_post = self.get_config_data.get_conf("shopDetail")
		shop_detail = self.send_post.send_post(params_post['url'], {}, params_post['header'])

		# 获取地址列表
		params_post = self.get_config_data.get_conf("getUserAddress")
		data = {"lat": shop_detail['data']['lat'], "lat": shop_detail['data']['lon']}
		params = self.send_post.send_post(params_post['url'], data, params_post['header'])
		# 选取满足条件的地址
		choice_address = []
		for address_post in params['data']:
			if address_post['usual'] == 1:
				choice_address.append(address_post)
		if not choice_address:
			return 500
		address_data = random.choice(choice_address)
		params_post = self.get_config_data.get_conf("getDistancePic")
		price_data = {"time": 0, "lat": address_data['lat'], "lon": address_data['lon']}
		price_params = self.send_post.send_post(params_post['url'], price_data, params_post['header'])
		service_fee = price_params['data']['totalPrice']
		start_price = price_params['data']['startingPrice']
		return {"service_fee": service_fee, "start_price": start_price, 'address_id': address_data['id']}

	# 校验套餐的优惠券
	def validator_package_coupon(self, type, package, price, vip_price, box_price):
		if package['discountTop'] == 1:  # 上不封顶
			discount = random.choice(package['discount'])
			if type in [2, 3, 5]:
				num = int((price + box_price) / (int(discount['amount'])))
				vip_num = int((vip_price + box_price) / (int(discount['amount'])))
				price = price - int(discount['discount']) * num
				vip_price = vip_price - int(discount['discount']) * vip_num
			else:
				num = int((price) / (int(discount['amount'])))
				vip_num = int((vip_price) / (int(discount['amount'])))
				price = price - int(discount['discount']) * num
				vip_price = vip_price - int(discount['discount']) * vip_num
		else:
			discount_money = 0
			vip_discount_money = 0
			for discount in package['discount']:
				if type in [2, 3, 5]:
					if int(price + box_price) > int(discount['amount']) and discount_money < int(
							discount['discount']):
						discount_money = int(discount['discount'])
					if int(vip_price + box_price) > int(discount['amount']) and vip_discount_money < int(
							discount['discount']):
						vip_discount_money = int(discount['discount'])
				else:
					if price > int(discount['amount']) and discount_money < int(discount['discount']):
						discount_money = int(discount['discount'])
					if vip_price > int(discount['amount']) and vip_discount_money < int(discount['discount']):
						vip_discount_money = int(discount['discount'])
			price = price - discount_money
			vip_price = vip_price - vip_discount_money

		return {"price": price, "vip_price": vip_price}

	# 设置写入空值情况
	def set_none_yam(self, ret, data, params, model, report = "", status = 500):
		result_status = {"key": [], "val": [], 'report': report}
		if not params:
			params = {'data': {}, 'status': 200, 'code': 0, 'message': '', 'request_time': 0, 'traceid': 0,
				'report_status': status}
		else:
			params['report_status'] = status
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)


if __name__ == '__main__':
	run = SetOrder()
	ret = run.set_shop_wm()
	print(ret)
