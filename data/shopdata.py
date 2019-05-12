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


class ShopData:

	def __init__(self):
		self.get_yaml_data = GetYaml()
		self.get_html_data = GetHtml()
		self.send_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_config_data = GetDataConfig()

	# 城市列表
	def city_list(self, model = [], post_data = None):
		file_path = "/public/yaml/shop/city_list.yaml"
		ret = self.get_config_data.get_data_post("cityList", file_path)
		url = ret['url']
		header = ret['header']
		if post_data is None:
			post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)
			if result_status == 'fail':
				continue
			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 获取商家列表(启动页面)
	def list(self, model = []):
		file_path = "/public/yaml/shop/list.yaml"
		ret = self.get_config_data.get_data_post("shopList", file_path)
		url = ret['url']
		post_data = ret['expect']['retData']

		# 获取城市列表
		header = self.get_config_data.get_conf("cityList")
		city_result = self.send_post.send_post(header['host'] + header['uri'], {"lon": 0, "lat": 0}, header['header'])
		if city_result['status'] == 500 or not city_result['data']:
			return False
		city_key = random.choice(list(city_result['data']['cityList']))
		# 循环用例，请求获取数据
		total = 0
		for data in post_data:
			if 'error' not in data:
				data['cityId'] = city_key
			page_data = self.validator.set_page(data, total)
			data['page'] = page_data['page']
			page_size = page_data['page_size']
			params = self.send_post.send_post(url, data, ret['header'])
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				continue

			# 特殊值断言
			report = ""
			if params['data']:
				total = params['data']['total']
				report += self.validator.page(page_size, params['data']['total'], params['data']['list'], data)
				# 断言数量
				if data['query'] is None and (
						int(city_result['data']['cityList'][city_key]['count']) != int(params['data'][
																						   'total'])):
					report += "城市ID" + str(city_key) + "在city_list统计为,total=" + \
							  str(city_result['data']['cityList'][city_key][
									  'count']) + "，在shop_list里为:" + str(params['data']['total']) + '<br/>'
					params['report_status'] = 202
				for result_data in params['data']['list']:
					if data['query']:
						if data['query'] not in result_data['name']:
							report += str(result_data['name']) + "不在搜索城市中，cityId=" + str(data['query']) + '<br/>'
							params['report_status'] = 202
							continue
					if int(result_data['cityId']) != int(data['cityId']):
						report = report + "门店名【" + str(result_data['name']) + "】,cityId:" + str(
								result_data['cityId']) + "不在此城市中，cityId=" + str(data['cityId']) + "<br/>"
						params['report_status'] = 202
			else:
				report += "没有相关门店，query=" + str(data['query'])
			result_status['report'] = report
			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 获取商家详情
	def detail(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/shop/detail.yaml"
		ret = self.get_config_data.get_data_post("shopDetail", file_path)
		url = ret['url']
		header = ret['header']
		data = {'cases_text': "店铺详情"}

		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
		if result_status == 'fail':
			return 500

		# 特殊值断言
		report = ""
		if params['data']:
			if int(params['data']['id']) != int(header['sid']):
				report += "门店【" + str(params['data']['name']) + "】,sid:" + str(
						params['data']['id']) + "结果不对目标门店，sid=" + str(header['sid']) + "<br/>"
				params['report_status'] = 204
		else:
			report = report + "没有相关门店，sid=" + header['sid']

		result_status['report'] = report
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# wifi列表
	def wifi_list(self):
		# 获取文件请求数据
		file_path = "/public/yaml/shop/wifi_list.yaml"
		ret = self.get_config_data.get_data_post("getWifiSetting", file_path)
		# 组装请求数据
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			result = 200
			# 请求api获取结果
			params = self.send_post.send_post(url, data, header)

			# 判断status
			result_status = self.validator.validate_status(ret['expect'], params, '店铺', url, data)
			if result_status == 'fail':
				continue

			# 特殊值断言
			report = ""
			if params['data']['list']:
				for result_data in params['data']['list']:
					if data['status'] != result_data['status']:
						report += str(result_data['name']) + "使用状态错误，status=" + str(result_data['status']) + '<br/>'
						result = 202
			else:
				report += "没有门店wifi"
			# 写入html
			self.get_html_data.set_html('店铺', url, data, result, params['message'], report)

		return result

	# 打赏配置
	def reward_set(self, model):
		file_path = "/public/yaml/shop/reward_set.yaml"
		ret = self.get_config_data.get_data_post("getRewardSet", file_path)
		url = ret['url']
		header = ret['header']
		data = {"cases_text": "获取打赏配置"}

		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)
		if result_status == 'fail':
			return False

		# 特殊值断言
		report = ""
		if not params['data']:
			report += "没有设置打赏配置"

		result_status['report'] = report
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 品牌故事
	def story_detail(self, model):
		file_path = "/public/yaml/shop/story_detail.yaml"
		ret = self.get_config_data.get_data_post("storyDetail", file_path)
		url = ret['url']
		header = ret['header']
		data = {'cases_text': "品牌故事"}

		params = self.send_post.send_post(url, data, header)
		result_status = self.validator.validate_status(ret, params, model, data)
		if result_status == 'fail':
			return 500

		# 特殊值断言
		report = ""
		if params['data']:
			if int(params['data']['sid']) != int(header['sid']):
				report += "门店故事查询错误，sid=" + str(params['data']['sid']) + '<br/>'
				params['report_status'] = 202
			if int(params['data']['is_del']) != 2:
				report += "门店故事查询错误，此内容已被删除，is_del=" + str(params['data']['is_del']) + '<br/>'
				params['report_status'] = 202
		else:
			report += "没有门店信息"

		result_status['report'] = report
		self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 商家桌位详情
	def table_list(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/shop/table_list.yaml"
		ret = self.get_config_data.get_data_post("tableList", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']
		exect_data = ret['expect']['result']['data']['list']

		# 循环用例，请求获取数据
		total = 0
		for data in post_data:
			# 请求api获取结果
			page_data = self.validator.set_page(data, total)
			data['page'] = page_data['page']
			page_size = page_data['page_size']

			params = self.send_post.send_post(url, data, header)
			dict_val = self.validator.set_dict_list(exect_data, params['data']['list'])
			params['data']['list'] = dict_val['params']
			ret['expect']['result']['data']['list'] = dict_val['data']
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				return 500
			total = params['data']['total']
			report = self.validator.page(page_size, params['data']['total'], params['data']['list'], data)
			result_status['report'] = report
			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 商家桌位详情
	def table_detail(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/shop/table_detail.yaml"
		ret = self.get_config_data.get_data_post("getStoreTableDetail", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']
		# 获取桌位
		params_post = self.get_config_data.get_conf("tableList")
		table_list = self.send_post.send_post(params_post['url'], {"status": 1}, params_post['header'])
		if table_list['status'] != 200 or not table_list['data']:
			return False
		dict_val = self.validator.set_dict_list(table_list['data']['list'], table_list['data']['list'])
		table_one = random.choice(dict_val['data'])
		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			if data['qrCode']:
				data['qrCode'] = table_one['qrCode']
			if data['tid']:
				data['tid'] = table_one['id']
			params = self.send_post.send_post(url, data, header)

			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				return 500

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 用户扫桌位码占桌
	def table_set_status(self, model):
		# 获取文件请求数据
		file_path = "/public/yaml/shop/table_set_status.yaml"
		ret = self.get_config_data.get_data_post("setTableStatus", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 获取桌位
		params_post = self.get_config_data.get_conf("tableList")
		table_list = self.send_post.send_post(params_post['url'], {"status": 1}, params_post['header'])
		if table_list['status'] != 200 or not table_list['data']:
			return False
		dict_val = self.validator.set_dict_list(table_list['data']['list'], table_list['data']['list'])
		table_one = random.choice(dict_val['data'])

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			data['tid'] = table_one['id']
			data['uid'] = ret['header']['uid']
			params = self.send_post.send_post(url, data, header)

			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				return 500

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True


if __name__ == '__main__':
	run = ShopData()
	res_data = run.list('启动页')
	print(res_data)
