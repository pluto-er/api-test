import os
import sys
import time
import random

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录

sys.path.append(root_path)

from main.goods import Goods
from main.msg import Msg
from main.shop import Shop
from main.startup import Startup
from main.user import User
from helper.get_html import GetHtml
from lib.global_val import glo
from helper.get_yaml import GetYaml


class UserMain:

	def __init__(self):
		self.startup = Startup()
		self.goods = Goods()
		self.shop = Shop()
		self.user = User()
		self.msg = Msg()
		self.get_html_data = GetHtml()
		glo.__init__(self)

	def start_main(self):
		file_name = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '-' + str(
				random.randint(10, 99))
		GetYaml.init_file(file_name)
		# 开始执行
		self.startup.start_up()  # 启动页面
		# self.shop.start_up()
		# self.goods.start_up()
		# self.user.user_all()
		# self.msg.start_up()

		# 写入html文件
		# self.get_html_data.set_html()


if __name__ == '__main__':
	run = UserMain()
	run.start_main()
