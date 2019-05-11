import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录

sys.path.append(root_path)

from data.shopdata import ShopData
from helper.get_html import GetHtml
from helper.get_config import GetDataConfig


class Startup:

	def __init__(self):
		self.shop = ShopData()
		self.get_html_data = GetHtml()
		self.get_config_data = GetDataConfig()

	def start_up(self):
		model = "启动页"

		try:
			self.shop.city_list([model, '城市列表'])
		except Exception as e:
			self.get_config_data.get_error_base('cityList', [model, '城市列表'], e)
		try:
			self.shop.list([model, '城市门店'])
		except Exception as e:
			self.get_config_data.get_error_base('shopList', [model, '城市门店'], e)


if __name__ == '__main__':
	run = Startup()
	run.start_up()
