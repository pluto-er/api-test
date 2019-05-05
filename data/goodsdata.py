# coding:utf-8
import sys
import os
import datetime
import random
import time

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from helper.get_yaml import GetYaml
from helper.get_html import GetHtml
from helper.request_post import SendPost
from helper.validator import ValidatorHelper
from helper.get_config import GetDataConfig


# from datetime import datetime


class GoodsData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()

	# 获取配置
	def config(self, model):
		file_path = "/public/yaml/goods/config.yaml"
		ret = self.get_config_data.get_data_post("foodsConfigInfo", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			params = self.send_post.send_post(url, data, header)

			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				return 500

			# 特殊值断言
			report = ""
			if not params['data']:
				report += "没有菜品配置"

			result_status['report'] = report
			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 菜品推荐-列表
	def recommend_list(self, model):
		file_path = "/public/yaml/goods/recommend_list.yaml"
		ret = self.get_config_data.get_data_post("recommendList", file_path)
		url = ret['url']
		header = ret['header']
		data = []

		# 请求api获取结果
		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status

		# 特殊值断言
		report = ""
		if not params['data']:
			report += "没有推荐菜品"

		result_status['report'] = report
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 菜品推荐-详情
	def recommend_one(self, model):
		file_path = "/public/yaml/goods/recommend_one.yaml"
		ret = self.get_config_data.get_data_post("recommendDetail", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 获取菜品推荐列表
			recommend_list = self.recommend_list(model)
			for recommend_data in recommend_list['data']:
				data['id'] = recommend_data['id']
				params = self.send_post.send_post(url, data, header)
				result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
				if result_status == 'fail':
					return 500

				self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 广告位列表
	def advertising_list(self, model):
		file_path = "/public/yaml/goods/advertising_list.yaml"
		ret = self.get_config_data.get_data_post("getAdListData", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)

			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				return 500

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 点餐-菜品分类列表
	def category_list(self, model, post_data = None):
		# 获取文件请求数据
		file_path = "/public/yaml/goods/category_list.yaml"
		ret = self.get_config_data.get_data_post("getCateListUrl", file_path)
		url = ret['url']
		header = ret['header']
		if not post_data:
			post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 点餐-菜品列表
	def list_index(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/goods/list_index.yaml"
		ret = self.get_config_data.get_data_post("getGoodsListUrl", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		for data in post_data:
			# 请求api获取结果
			category_list = self.category_list(model, [{"type": data['type']}])
			if not category_list['data']['list']:
				continue

			for list_data in category_list['data']['list']:
				data['cid'] = list_data['id']

				params = self.send_post.send_post(url, data, header)
				result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
				if result_status == 'fail':
					continue

				self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 点餐-菜品列表
	def goods_list_index(self, model, post_data = None):
		# 获取文件请求数据
		file_path = "/public/yaml/goods/list_index.yaml"
		ret = self.get_config_data.get_data_post("getGoodsListUrl", file_path)
		url = ret['url']
		header = ret['header']
		if not post_data:
			post_data = ret['expect']['retData']

		for data in post_data:
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 点餐-获取菜品规格
	def spec(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/goods/spec.yaml"
		ret = self.get_config_data.get_data_post("getGoodsDetailUrl", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			order_type = [1, 2, 3]
			for type_data in order_type:
				goods_list = self.get_goods(model, type_data, [2])
				if not goods_list:
					continue

				for goods_data in goods_list:
					data['glid'] = goods_data['id']
					data['type'] = type_data

					# 请求api获取结果
					params = self.send_post.send_post(url, data, header)
					result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
					if result_status == 'fail':
						continue

					self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 点餐-获取菜品规格
	def get_spec(self, model, post_data = None):
		# 获取文件请求数据
		file_path = "/public/yaml/goods/spec.yaml"
		ret = self.get_config_data.get_data_post("getGoodsDetailUrl", file_path)
		url = ret['url']
		header = ret['header']
		if not post_data:
			post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 检查菜品是否正常，返回不正常数据
	def check(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/goods/check.yaml"
		ret = self.get_config_data.get_data_post("checkGoodsStatusList", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			for type_data in [1, 2, 3]:
				for goods_type in [1, 2, 3]:
					goods_list = self.get_goods(model, type_data, [goods_type])
					if not goods_list:
						continue

					for goods_data in goods_list:
						data['glid'] = goods_data['id']
						data['type'] = type_data
						data['num'] = goods_data['min']

						# 请求api获取结果
						params = self.send_post.send_post(url, data, header)
						result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
						if result_status == 'fail':
							continue

						self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 点餐-加购提醒
	def addition(self, model):
		file_path = "/public/yaml/goods/addition.yaml"
		ret = self.get_config_data.get_data_post("getAddSlpListUrl", file_path)
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

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 套餐详情
	def package(self, model):
		file_path = "/public/yaml/goods/package.yaml"
		ret = self.get_config_data.get_data_post("getPackageDetailUrl", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 获取套餐
			order_type = [1, 2, 3]
			for type_data in order_type:
				goods_list = self.get_goods(model, type_data, [3])
				if not goods_list:
					continue
				for goods_data in goods_list:
					data['glid'] = goods_data['id']
					data['type'] = type_data
					# 请求api获取结果
					params = self.send_post.send_post(url, data, header)
					result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
					if result_status == 'fail':
						continue

					self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 套餐详情
	def get_package(self, model, post_data = None):
		file_path = "/public/yaml/goods/package.yaml"
		ret = self.get_config_data.get_data_post("getPackageDetailUrl", file_path)
		url = ret['url']
		header = ret['header']
		if not post_data:
			post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 点餐先行条件
	def get_shopping(self, shop_type = 1, goods_type = [1], shop_reserve_data = 1, send_time = 0):
		# # shop_type 1堂食 2外带 3外卖 goods_type 1单品 2多规格 3套餐
		params = self.category_list(['下单', '分类列表'], [{'type': [shop_type]}])
		if 'list' not in params['data']:
			return False
		if not params['data']['list']:
			return False
		del params['data']['list'][0]  # 删除菜品推荐

		goods_result = []
		goods_id = []
		for result_data in params['data']['list']:
			goods_list = self.goods_list_index(['下单', '分类列表'], [{'cid': result_data['id'], 'type': [shop_type]}])
			for goods_data in goods_list['data']:
				if goods_data['id'] in goods_id:  # 去重
					continue
				if shop_reserve_data == 2 and goods_data['saleTime'] == 2:  # 预订单
					if send_time:
						reserve_status = self.decide_reserve_time(send_time, goods_data)  # 判断预订单菜品是否可用
						if reserve_status == 2:
							goods_data['isSale'] = 2
				goods_id.append(goods_data['id'])  # 加入goods_id列表
				if int(goods_data['type']) != 1 and goods_data['type'] in goods_type:
					goods_data['detail'] = {}
					if goods_data['type'] == 2:  # 获取多规格详情
						goods_spec_data = self.get_spec(['下单', '规格详情'], [{"glid": goods_data['id']}])
						goods_data['detail'] = goods_spec_data['data']
					elif goods_data['type'] == 3:  # 获取套餐详情
						goods_spec_data = self.get_package(['下单', '规格详情'], [{"glid": goods_data['id']}])
						goods_data['detail'] = goods_spec_data['data']
					goods_result.append(goods_data)
		return goods_result

	# 点餐加购先行条件

	def get_addition(self, shop_type = 1):  # shop_type 1堂食 2外带 3外卖
		config = self.get_config_data.get_conf("getAddSlpListUrl")
		# 获取分类
		url = config['host'] + config['uri']
		header = config['header']
		data = {'type': shop_type}
		params = self.send_post.send_post(url, data, header)

		return params

	# 获取预定时间(是否可用)
	def decide_reserve_time(self, send_time = "", sale_time_limit = []):
		# 获取当前周几
		is_status = 2
		time_strftime = time.strptime(send_time, "%Y-%m-%d %H:%M:%S")
		worker = time_strftime.tm_wday + 1
		date_time = str(time_strftime.tm_hour).rjust(2, '0') + ":" + str(time_strftime.tm_min).rjust(2, '0')
		for data in sale_time_limit['saleTimeLimit']:
			if worker not in data['week']:
				continue
			for time_data in data['time']:
				if time_data['start'] <= date_time <= time_data['end']:
					is_status = 1

		return is_status

	# 点餐先行条件
	def get_goods(self, model, shop_type, goods_type):
		# # shop_type 1堂食 2外带 3外卖 goods_type 1单品 2多规格 3套餐
		params = self.category_list([model[0], '菜品分类列表'], [{'type': [shop_type]}])
		if not params['data']['list']:
			return False
		del params['data']['list'][0]  # 删除菜品推荐

		goods_result = []
		goods_id = []
		for result_data in params['data']['list']:
			goods_list = self.goods_list_index([model[0], '菜品列表'], [{'cid': result_data['id'], 'type': [shop_type]}])
			for goods_data in goods_list['data']:
				if goods_data['id'] in goods_id:  # 去重
					continue
				goods_id.append(goods_data['id'])  # 加入goods_id列表
				if goods_data['type'] in goods_type:
					goods_result.append(goods_data)
		return goods_result


if __name__ == '__main__':
	run = GoodsData()
	ret = run.package(['套餐', '套餐详情'])
	print(ret)
