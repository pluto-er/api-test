# coding:utf-8
import sys
import os
import random
import datetime
import time

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from helper.request_post import SendPost
from helper.get_config import GetDataConfig
from helper.set_order import SetOrder


class GetPremise:

	def __init__(self):
		self.send_post = SendPost()
		self.get_config_data = GetDataConfig()
		self.set_order = SetOrder()

	# 获取店铺详情
	def get_shop_detail(self):
		file_path = "/public/yaml/shop/detail.yaml"
		ret = self.get_config_data.get_data_post("shopDetail", file_path)
		url = ret['url']
		header = ret['header']
		data = []

		params = self.send_post.send_post(url, data, header)
		if params['status'] == 500 or not params['data']:
			return False
		return params

	# 获取用户详情
	def get_user_info(self):
		file_path = "/public/yaml/user/info.yaml"
		ret = self.get_config_data.get_data_post("getUserInfo", file_path)
		url = ret['url']
		header = ret['header']
		data = []

		params = self.send_post.send_post(url, data, header)
		# if params['status'] == 500 or not params['data']:
		# 	return False
		return params

	# 获取菜品列表
	def get_goods_list(self, type):
		# 获取菜品列表
		result = []
		header = self.get_config_data.get_conf("getCateListUrl")
		params = self.send_post.send_post(header['host'] + header['uri'], {"type": [type]}, header['header'])
		if not params['data']:
			return False

		header = self.get_config_data.get_conf("getGoodsListUrl")
		for cid_data in params['data']['list']:
			if not cid_data['id']:
				continue

			data = {"cid": cid_data['id'], 'type': [type]}
			list_data = self.send_post.send_post(header['host'] + header['uri'], data, header['header'])
			if not list_data['data']:
				continue

			for goods in list_data['data']:
				result.append(goods)

		return result

	"""
	获取预定时间
	:type 1堂食 3外卖 4自提
	"""

	def get_send_time(self, type):
		if type == 5:
			type = 4
		header = self.get_config_data.get_conf("getStoreDistributionList")
		params = self.send_post.send_post(header['host'] + header['uri'], {"type": type}, header['header'])
		if not params['data']:
			return False

		ret_date = random.choice(params['data'])
		ret_time = ret_date['date'] + " " + random.choice(ret_date['timeList'])
		ret_time = int(time.mktime(time.strptime(ret_time, "%Y-%m-%d  %H:%M")))
		ret_time_error = ret_time + 86400 * 7

		return [{"status": 1, "time": ret_time}, {"status": 2, "time": ret_time_error}]

	"""
	加购
	status 0默认(都选)  1非必选不选 2 必选不选 3 非必选和必选都不选
	"""

	def add_goods_shop(self, type, status = 0):
		if type == 4:
			type = 1
		elif type == 5:
			type = 2
		header = self.get_config_data.get_conf("getAddSlpListUrl")
		params = self.send_post.send_post(header['url'], {"type": type}, header['header'])
		if not params['data']:
			return False
		add_goods_result = []
		for goods_add_data in params['data']['required']:
			if status == 2 or status == 3:
				continue
			if goods_add_data['vipPrice'] == 0:
				goods_add_data['vipPrice'] = goods_add_data['price']
			add_goods_list = {
				"id": int(goods_add_data['id']),
				"number": goods_add_data['min'],
				"type": goods_add_data['type'],
				"vipPrice": goods_add_data['vipPrice'],
				"price": goods_add_data['price'],
				"boxPrice": goods_add_data['boxPrice'],
				'goodsCouponId': 0,
				'attributes': [],
				'status': 1  # 必选
				}
			add_goods_result.append(add_goods_list)

		for goods_add_data in params['data']['option']:
			if status == 1 or status == 3:
				continue
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
				'attributes': [],
				'status': 0  # 非必选
				}
			add_goods_result.append(add_goods_list)

		return add_goods_result

	"""
	获取联系方式，随便写入一个电话号码
	"""

	def picked_up_info(self):
		header = self.get_config_data.get_conf("getUserSelfMobile")
		params = self.send_post.send_post(header['host'] + header['uri'], {}, header['header'])
		if params['status'] != 200:
			return False

		if params['data']:
			return params['data']['id']

		header = self.get_config_data.get_conf("saveUserSelfMobile")
		params = self.send_post.send_post(header['host'] + header['uri'], {"mobile": "18281614323"}, header['header'])
		if params['status'] != 200:
			return False
		return params['data']['id']

	"""
	获取优惠券列表
	"""

	def coupon_list(self):
		params_post = self.get_config_data.get_conf("getAvailableCoupon")
		coupon_list = self.send_post.send_post(params_post['url'], {}, params_post['header'])
		if coupon_list['status'] != 200 or not coupon_list['data'] or not coupon_list['data']['coupon']:
			return []
		coupon_data = coupon_list['data']['coupon']

		return coupon_data

	# 员工列表
	def worker_list(self):
		header = self.get_config_data.get_conf("workerList")
		worker = self.send_post.send_post(header['host'] + header['uri'], {}, header['header'])
		if worker['status'] != 200 or not worker['data']:
			return False
		worker_list = []
		if worker['data']['manager']:
			worker['data']['manager']['manager_status'] = 1
			worker_list.append(worker['data']['manager'])
		if worker['data']['workerList']:
			worker_list.append(random.choice(worker['data']['workerList']))
		if not worker_list:
			return False
		return worker_list  # 员工列表

	def get_comment_list(self, data):
		header = self.get_config_data.get_conf("commentList")
		comment = self.send_post.send_post(header['host'] + header['uri'], data, header['header'])
		if not comment['data']['list']:
			comment_post_data = [
				{"type": random.choice([1, 3, 4]), "star": random.randint(1, 5), "page": 1, "size": 5, "state": 1}]
			self.get_comment_list(comment_post_data)
		result = {"data": comment, "post": data}
		return result

	# 获取菜品  status 1不支持当前方式  2不可售 3库存不足
	def get_goods(self, type = 1, goods_type = [1], status = 0):
		result = []
		# 获取菜品
		goods_list = self.get_goods_list(type)

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
			if status == 1 and goods[shop_type] == 2:  # 不支持对应方式
				result.append(goods)
			elif status == 2 and goods[shop_type] == 1 and goods['isSale'] == 2 \
					and int(goods['stock']) >= goods['min']:  # 不可售
				result.append(goods)
			elif status == 3 and goods[shop_type] == 1 and goods['isSale'] == 1 and int(goods['stock']) < goods[
				'min']:  # 库存不足
				result.append(goods)
			elif status == 0 and goods[shop_type] == 1 and goods['isSale'] == 1 and int(goods['stock']) >= goods[
				'min']:  # 充足条件
				result.append(goods)
		return result

	# 获取套餐
	# 1必选单选/其他选1 2必选多选/其他选1 3 必选不选/其他选1
	# 4 非必单选（必选选择）  5非必选多选（必选选择） 6 非必选不选（必选选择）
	def get_package(self, type, post_data):
		goods = self.get_goods(type, [3])
		package_result = []
		result = []
		price = vip_price = box_price = 0
		if type in [1, 4]:
			key = "dineIn"
		elif type in [2, 5]:
			key = "takeAway"
		else:
			key = "takeOut"
		for goods_data in goods:
			header = self.get_config_data.get_conf("getPackageDetailUrl")
			package = self.send_post.send_post(header['url'], {"glid": goods_data['id']}, header['header'])
			# 1 正常
			for package_data in package['data']['package']['list']:
				package_parts_data = []
				for package_parts in package_data['parts']:
					package_parts['attributes'] = []
					if package_parts['type'] == 2:
						spac = random.choice(package['data']['property'][str(package_parts['gid'])])
						spac_v = random.choice(spac['list'])
						package_parts['attributes'] = [{"id": spac_v['gpid'],
							"valueId": spac_v['id']}]
					if package_parts['isSale'] == 1 and package_parts['stock'] > package_parts['min'] \
							and package_parts[key] == 1:
						package_parts_data.append(package_parts)

				if post_data == 1:
					if package_data['option'] == 1:
						package_result.append(random.choice(package_parts_data))
					else:
						package_result.append(random.choice(package_parts_data))
				if post_data == 2:
					if package_data['option'] == 1:
						for parts_data in package_parts_data:
							package_result.append(parts_data)
					else:
						package_result.append(random.choice(package_parts_data))
				if post_data == 3:
					if package_data['option'] != 1:
						package_result.append(random.choice(package_parts_data))
				if post_data == 4:
					if package_data['option'] == 1:
						package_result.append(random.choice(package_parts_data))
					else:
						package_result.append(random.choice(package_parts_data))
				if post_data == 5:
					if package_data['option'] == 1:
						package_result.append(random.choice(package_parts_data))
					else:
						for parts_data in package_parts_data:
							package_result.append(parts_data)
				if post_data == 6:
					if package_data['option'] == 1:
						package_result.append(random.choice(package_parts_data))
			goodsList = []
			for goods_package in package_result:
				goodsList.append({
					"attributes": goods_package['attributes'],
					"groupId": goods_package['gpid'],
					"id": goods_package['gid'],
					"number": goods_package['min'],
					"price": goods_package['price'],
					"vipPrice": goods_package['vipPrice'],
					"boxPrice": goods_package['boxPrice'],
					"type": goods_package['type']})
				price = price + (int(goods_package['price']) * int(goods_package['min']))
				vip_price = vip_price + goods_package['vipPrice'] * goods_package['min']
				box_price = box_price + goods_package['boxPrice'] * goods_package['min']
			# 满减
			if package['data']['package']['discountTips'] == 1 and package['data']['package']['discount']:
				package_count = self.set_order.validator_package_coupon(type, package['data']['package'],
																		price, vip_price, box_price)
				price = package_count['price']
				vip_price = package_count['vip_price']
		result.append({"id": goods_data['gid'], "number": 1, "type": 3, "goodsList": goodsList})

		return {"goods": result, "price": price, "vip_price": vip_price, "box_price": box_price}

	# 加购
	def get_add_goods(self, type, status = 0):
		add_goods_price = add_goods_vip_price = add_goods_box_price = 0
		add_goods = self.add_goods_shop(type, status)
		for add_goods_data in add_goods:
			add_goods_price = add_goods_price + add_goods_data['price'] * add_goods_data['number']
			add_goods_vip_price = add_goods_vip_price + add_goods_data['vipPrice'] * add_goods_data['number']
			add_goods_box_price = add_goods_box_price + add_goods_data['boxPrice'] * add_goods_data['number']
		add_goods_return = {"add_goods": add_goods, "add_goods_price": add_goods_price,
			"add_goods_vip_price": add_goods_vip_price, "add_goods_box_price": add_goods_box_price}
		return add_goods_return

	# 获取，能正常下单的菜品
	def get_order_goods(self, type, goods_type = [1], add_status = 0):
		goods_data = self.get_goods(type, goods_type)
		price = vip_price = box_price = 0
		add_goods_price = add_goods_vip_price = add_goods_box_price = 0
		goods_params = []
		for goods in goods_data:
			if type in [2, 5] and goods['takeAway'] == 2:
				continue
			elif type in [1, 4] and goods['dineIn'] == 2:
				continue
			elif type == 3 and goods['takeOut'] == 2:
				continue

			goods_post = self.set_order.add_goods_type_single(goods)
			goods_params.append(goods_post)
			price = price + goods_post['price'] * goods_post['number']
			vip_price = vip_price + goods_post['vipPrice'] * goods_post['number']
			box_price = box_price + goods_post['boxPrice'] * goods_post['number']
		goods_return = {"goods": goods_params, "price": price, "vip_price": vip_price, "box_price": box_price}
		# 加购
		add_goods = self.add_goods_shop(type, add_status)
		for add_goods_data in add_goods:
			add_goods_price = add_goods_price + add_goods_data['price'] * add_goods_data['number']
			add_goods_vip_price = add_goods_vip_price + add_goods_data['vipPrice'] * add_goods_data['number']
			add_goods_box_price = add_goods_box_price + add_goods_data['boxPrice'] * add_goods_data['number']
		add_goods_return = {"add_goods": add_goods, "add_goods_price": add_goods_price,
			"add_goods_vip_price": add_goods_vip_price, "add_goods_box_price": add_goods_box_price}
		result = {
			"goodsList": goods_return,
			"addGoodsList": add_goods_return,
			}
		return result

	# 获取，能正常下单的菜品(预定单，目前只获取全时段的数据)
	def get_order_goods_reserve(self, type, goods_type = [1], add_status = 0):
		goods_data = self.get_goods(type, goods_type)
		price = vip_price = box_price = 0
		add_goods_price = add_goods_vip_price = add_goods_box_price = 0
		goods_params = []
		for goods in goods_data:
			if type in [2, 5] and goods['takeAway'] == 2:
				continue
			elif type in [1, 4] and goods['dineIn'] == 2:
				continue
			elif type == 3 and goods['takeOut'] == 2:
				continue
			if goods['isSale'] != 1 or goods['saleTime'] != 1:
				continue
			goods_post = self.set_order.add_goods_type_single(goods)
			goods_params.append(goods_post)
			price = price + goods_post['price'] * goods_post['number']
			vip_price = vip_price + goods_post['vipPrice'] * goods_post['number']
			box_price = box_price + goods_post['boxPrice'] * goods_post['number']
		goods_return = {"goods": goods_params, "price": price, "vip_price": vip_price, "box_price": box_price}
		# 加购
		add_goods = self.add_goods_shop(type, add_status)
		for add_goods_data in add_goods:
			add_goods_price = add_goods_price + add_goods_data['price'] * add_goods_data['number']
			add_goods_vip_price = add_goods_vip_price + add_goods_data['vipPrice'] * add_goods_data['number']
			add_goods_box_price = add_goods_box_price + add_goods_data['boxPrice'] * add_goods_data['number']
		add_goods_return = {"add_goods": add_goods, "add_goods_price": add_goods_price,
			"add_goods_vip_price": add_goods_vip_price, "add_goods_box_price": add_goods_box_price}
		result = {
			"goodsList": goods_return,
			"addGoodsList": add_goods_return,
			}
		return result

	def get_order_list(self, data = {}):
		file_path = "/public/yaml/order/list.yaml"
		ret = self.get_config_data.get_data_post("getOrderList", file_path)
		url = ret['url']
		header = ret['header']

		params = self.send_post.send_post(url, data, header)
		if params['status'] == 500 or not params['data']:
			return False
		return params

	# 获取标签列表
	def get_label_list(self, type):
		file_path = "/public/yaml/comment/get_label_list.yaml"
		ret = self.get_config_data.get_data_post("getOrderCommentTags", file_path)
		url = ret['url']
		header = ret['header']

		params = self.send_post.send_post(url, {"type": type}, header)
		if params['status'] == 500 or not params['data']:
			return False

		return params


if __name__ == '__main__':
	run = GetPremise()
	ret = run.get_package(5, 1)
	print(ret)
