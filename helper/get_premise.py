# coding:utf-8
import sys
import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from helper.request_post import SendPost
from helper.get_config import GetDataConfig


class GetPremise:

	def __init__(self):
		self.send_post = SendPost()
		self.get_config_data = GetDataConfig()

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
		if params['status'] == 500 or not params['data']:
			return False
		return params

	def get_goods_list(self, type):
		# 获取菜品列表
		result = []
		header = self.get_config_data.get_conf("getCateListUrl")
		params = self.send_post.send_post(header['host'] + header['uri'], {"type": [type]}, header['header'])
		if not params['data']['list']:
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


if __name__ == '__main__':
	run = GetPremise()
	ret = run.get_shop_detail()
	print(ret)
