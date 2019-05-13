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
from data.order import OrderData


class UserMain:

	def __init__(self):
		self.startup = Startup()
		self.goods = Goods()
		self.shop = Shop()
		self.user = User()
		self.msg = Msg()
		self.get_html_data = GetHtml()
		self.order = OrderData()
		glo.__init__(self)

	def start_main(self):
		file_name = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '-' + str(
				random.randint(10, 99))
		GetYaml.init_file(file_name)
		# 开始执行
		# self.startup.start_up()  # 启动页面
		# self.shop.start_up()  # 店铺相关
		# self.goods.my_data()  # 菜品列表
		# self.goods.my_order()  # 点餐-确认页
		# self.goods.pay_success()  # 支付完成
		# self.goods.poster()  # 广告位
		# self.msg.start_up()  # 消息
		# self.user.my_user()
		# self.user.my_coupon()
		# self.user.my_recharge()
		# self.user.my_invitations()
		# self.user.my_order()
		# self.order.add_order(1)  # 库存情况方式
		# self.order.add_order(2)  # 库存情况方式
		# self.order.add_order(3)  # 库存情况方式
		# self.order.add_order(4)  # 库存情况方式
		# self.order.add_order(5)  # 库存情况方式
		self.user.my_comment()

		# 写入html文件
		self.get_html_data.set_html()


if __name__ == '__main__':
	run = UserMain()
	run.start_main()
