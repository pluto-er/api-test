import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from data.commentdata import CommentData
from data.msgdata import MsgData
from data.coupondata import CouponData
from data.activitydata import ActivityData
from data.userdata import UserData
from data.invitationsdata import InvitationsData
from data.usercommentdata import UserCommentData
from data.orderdata import OrderData
from data.goodsdata import GoodsData
from data.shopdata import ShopData
from data.workerdata import WorkerData
from helper.get_html import GetHtml


class Goods:

	def __init__(self):
		self.msg = MsgData()
		self.comment = CommentData()
		self.coupon = CouponData()
		self.activity = ActivityData()
		self.user = UserData()
		self.invitations = InvitationsData()
		self.user_comment = UserCommentData()
		self.order = OrderData()
		self.goods = GoodsData()
		self.shop = ShopData()
		self.worker = WorkerData()
		self.get_html_data = GetHtml()

	# 点餐
	def my_data(self):
		model = "点餐"
		self.user.init_shop([model, '会员初始化'])
		self.shop.detail([model, '店铺详情'])
		self.user.info([model, '用户详情'])
		self.goods.category_list([model, '菜品分类'])
		self.goods.list_index([model, '菜品列表'])
		self.goods.package([model, '套餐详情'])
		self.goods.spec([model, '多规格'])

	# 点餐-确认订单
	def my_order(self):
		model = "点餐"
		# self.goods.check([model, '检验菜品'])  # 最好注释
		# self.goods.addition([model, '加购提醒'])
		self.shop.table_list([model, '座位详情'])
		self.shop.table_detail([model, '座位详情'])
		self.shop.table_set_status([model, '扫码占座'])
		self.coupon.coupon_able_list([model, '优惠券列表'])
		self.activity.recharge_list([model, '充值活动列表'])
		self.user.info([model, '用户详情'])
		self.user.init_shop([model, '会员初始化'])

	# 支付完成
	def add_order(self):
		model = "支付完成"
		self.shop.detail([model, "商户详情"])
		self.goods.check([model, "菜品检验"])
		self.order.detail([model, "订单详情"])
		self.coupon.coupon_get_share([model, "分享地址"])
		self.coupon.check_invite_conf([model, "邀请返现券"])
		self.coupon.coupon_goods_able_list([model, "菜品券列表"])

	# 广告位
	def poster(self):
		model = "广告位"
		self.goods.advertising_list([model, '广告位'])
		self.coupon.get_reg([model, '注册弹框'])

	def start_up(self):
		self.my_data()
		self.add_order()
		self.poster()
		self.my_order()


# self.add_order()


if __name__ == '__main__':
	run = Goods()
# run.my_data()
# run.my_order()
# run.add_order()
