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
from helper.get_yaml import GetYaml
from helper.get_html import GetHtml
from helper.request_post import SendPost
from helper.validator import ValidatorHelper
from helper.get_geo import GetGeo

from data.goodsdata import GoodsData
from data.userdata import UserData
from data.shopdata import ShopData
from data.addressdata import AddressData


class OrderData:

	def __init__(self):
		self.get_config_data = GetDataConfig()
		self.get_premise = GetPremise()
		self.get_yaml_data = GetYaml()
		self.send_post = SendPost()

	# 新增订单
	def add(self, model):
		# 获取就餐方式
		file_path = "/public/yaml/order/add.yaml"
		ret = self.get_config_data.get_data_post("postOrderUrl", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']
		# 获取基础数据
		shop_detail = self.get_premise.get_shop_detail()  # 获取店铺详情
		if not shop_detail:
			self.get_yaml_data.set_to_yaml(ret, [], shop_detail, model)
			return True
		user = self.get_premise.get_user_info()  # 获取用户信息
		if not user:
			self.get_yaml_data.set_to_yaml(ret, [], user, model)
			return True

		for data in post_data:  # 循环就餐类型
			# 判断当前就餐方式是否支持预订单
			shop_reserve = self.decide_reserve(data['type'], shop_detail['data']['bookExpand'])
			goods_type_list = [[1], [2], [3], [1, 2], [2, 3], [1, 3], [1, 2, 3]]

			for shop_reserve_data in shop_reserve:  # 1无预定、2预定
				if shop_reserve_data == 2:  # 预定
					for book_data in [1, 2]:  # 1及时单 2 预订单
						if book_data == 2:  # 及时单
							pass
							continue
						for goods_type_data in goods_type_list:
							if goods_type_data == [1]:  # 单品
								for goods_status in [1, 2]:  # 1自提外带 2不支持自提外带
									if goods_status == 2:
										pass
										continue
									for sale_time_data in [1, 2]:  # 1可售  2不可售
										if sale_time_data == 2:
											pass
											continue
										for stock_data in [1, 2]:  # 1库存充足 2库存不足
											if stock_data == 2:
												pass
												continue
											for goods_limit_data in [1, 2, 3, 4]:  # 1小于起购 2等于起购 3等于限购 4大于限购
												pass

				else:
					pass
		return True

	# type_status 1自提外带 2不支持自提外带
	# sale_status 1可售  2不可售

	def get_goods(self, type = 1, goods_type = [1], type_status = 0, sale_status = 0):
		result = []
		# 获取菜品
		goods_list = self.get_premise.get_goods_list(type)

		if not goods_list:
			return False
		# 转化就餐方式
		if type == 1:
			shop_type = "dineIn"
		elif type == 2:
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
			elif goods[shop_type] == 1 and goods['isSale'] == 1 and int(goods['stock']) < goods['min']:  # 库存不足
				result.append(goods)
			elif goods[shop_type] == 1 and goods['isSale'] == 1 and int(goods['stock']) >= goods['min']:  # 充足条件
				result.append(goods)
		return result

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

	# 新增订单
	def add_case(self):
		k = 1
		post_data = []
		for type_data in [4]:  # ["堂食", "外带", "外卖", "自提堂食", "自提外带"]
			for shop_time_data in [1, 2]:  # 1营业时间 2非营业时间
				for book_data in [1, 2]:
					pass
		# yaml = OperationYaml()
		# yaml.set('/public/yaml/order/addtest.yaml', post_data)
		exit()

	# 新增订单
	def add_caseold(self):
		k = 1
		post_data = []
		for type_data in [4]:  # ["堂食", "外带", "外卖", "自提堂食", "自提外带"]
			for book_data in [1, 2]:  # ["非预定", "预定"]
				for goods_type_data in [1, 2, 3, 4, 5, 6, 7]:
					# ["单品", "多规格", "套餐", "单品、多规格", "单品、套餐", "多规格、套餐","单品、多规格、套餐"]
					for sale_status_data in [1, 2, 3]:
						for spec_status_data in [1, 2]:
							for coupon_status_data in [1, 2, 3, 4]:

								if goods_type_data in [9]:
									for full_data in [1, 2, 3]:  # 1开启满减 2关闭满减 3上不封顶
										for attain_data in [1, 2]:  # 1满足满减条件 2不满足满减条件
											for limit_data in [1, 2]:  # 1不限购 2 限购
												for choice_type_data in [1, 2]:  # 1必选单选 2 必选多选  3非必选单选 4 非必选多选
													type_text = ["堂食", "外带", "外卖", "自提堂食", "自提外带"]
													book_text = ["非预定", "预定"]
													goods_text = ["单品", "多规格", "套餐", "单品、多规格", "单品、套餐", "多规格、套餐",
														"单品、多规格、套餐"]
													sale_text = ["正常可售时间", "不可售时间段", "库存/限量"]
													spec_text = ["不选加购产品", "勾选加购产品"]
													coupon_text = ["不使用优惠券", "使用优惠券", "使用了不可使用优惠券", "使用菜品券"]
													goods_type = [[1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
													data = {"type": 1, "book": 1,
														"goods_type": goods_type[goods_type_data - 1],
														"sale_status": 1, "spec_status": 1,
														"coupon_status": 1,
														"case_text": "测试【" + book_text[book_data - 1] +
																	 "】【" + coupon_text[coupon_status_data - 1] +
																	 "】在【" + sale_text[sale_status_data - 1] +
																	 "】情况下购买【" + goods_text[
																		 goods_type_data - 1] + "】商品，并【" + spec_text[
																		 spec_status_data - 1] + "】的【" +
																	 type_text[type_data - 1] + "】订单"
														}
													post_data.append(data)
													print(str(k) + str(data))
													k = k + 1
								else:
									type_text = ["堂食", "外带", "外卖", "自提堂食", "自提外带"]
									book_text = ["非预定", "预定"]
									goods_text = ["单品", "多规格", "套餐", "单品、多规格", "单品、套餐", "多规格、套餐", "单品、多规格、套餐"]
									sale_text = ["正常可售时间", "不可售时间段", "库存/限量"]
									spec_text = ["不选加购产品", "勾选加购产品"]
									coupon_text = ["不使用优惠券", "使用优惠券", "使用了不可使用优惠券", "使用菜品券"]
									goods_type = [[1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
									data = {"type": 1, "book": 1, "goods_type": goods_type[goods_type_data - 1],
										"sale_status": 1, "spec_status": 1,
										"coupon_status": 1,
										"case_text": "测试【" + book_text[book_data - 1] +
													 "】【" + coupon_text[coupon_status_data - 1] +
													 "】在【" + sale_text[sale_status_data - 1] +
													 "】情况下购买【" + goods_text[goods_type_data - 1] + "】商品，并【" + spec_text[
														 spec_status_data - 1] + "】的【" +
													 type_text[type_data - 1] + "】订单"
										}
									post_data.append(data)
									print(str(k) + str(data))
									k = k + 1
		# yaml = OperationYaml()
		# yaml.set('/public/yaml/order/addtest.yaml', post_data)
		exit()


if __name__ == '__main__':
	run = OrderData()
	ret = run.get_goods(2)
	print(ret)
	exit()
