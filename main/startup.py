import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录

sys.path.append(root_path)

from data.shopdata import ShopData
from helper.get_html import GetHtml


class Startup:

	def __init__(self):
		self.shop = ShopData()
		self.get_html_data = GetHtml()

	def start_up(self):
		model = "启动页"
		self.shop.city_list([model, '城市列表'])
		self.shop.list([model, '城市门店'])


if __name__ == '__main__':
	run = Startup()
	run.start_up()
