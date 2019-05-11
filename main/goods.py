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
from helper.get_config import GetDataConfig


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
		self.get_config_data = GetDataConfig()

	# 点餐列表
	def my_data(self):
		model = ["点餐", '菜品列表', 'user']
		try:
			self.user.init_shop(model)
		except Exception as e:
			self.get_config_data.get_error_base('initUserShop', model, e)
		try:
			self.user.info(model)
		except Exception as e:
			self.get_config_data.get_error_base('getUserInfo', model, e)
		model = ["点餐", '菜品列表', 'shop']
		try:
			self.shop.detail(model)
		except Exception as e:
			self.get_config_data.get_error_base('shopDetail', model, e)
		model = ["点餐", '菜品列表', 'goods']
		try:
			self.goods.category_list(model)
		except Exception as e:
			self.get_config_data.get_error_base('getCateListUrl', model, e)
		try:
			self.goods.list_index(model)
		except Exception as e:
			self.get_config_data.get_error_base('getGoodsListUrl', model, e)
		try:
			self.goods.package(model)
		except Exception as e:
			self.get_config_data.get_error_base('getPackageDetailUrl', model, e)
		try:
			self.goods.spec(model)
		except Exception as e:
			self.get_config_data.get_error_base('getGoodsDetailUrl', model, e)

	# 点餐-确认订单
	def my_order(self):
		model = "点餐"
		try:
			self.goods.check([model, '检验菜品', 'goods'])
		except Exception as e:
			self.get_config_data.get_error_base('checkGoodsStatusList', [model, '检验菜品', 'goods'], e)
		try:
			self.goods.addition([model, '加购提醒', 'goods'])
		except Exception as e:
			self.get_config_data.get_error_base('getAddSlpListUrl', [model, '加购提醒', 'goods'], e)
		try:
			self.shop.table_list([model, '座位详情', 'shop'])
		except Exception as e:
			self.get_config_data.get_error_base('tableList', [model, '座位详情', 'shop'], e)
		try:
			self.shop.table_detail([model, '座位详情', 'shop'])
		except Exception as e:
			self.get_config_data.get_error_base('getStoreTableDetail', [model, '座位详情', 'shop'], e)
		try:
			self.shop.table_set_status([model, '扫码占座', 'shop'])
		except Exception as e:
			self.get_config_data.get_error_base('setTableStatus', [model, '扫码占座', 'shop'], e)
		try:
			self.coupon.coupon_able_list([model, '优惠券列表', 'activity'])
		except Exception as e:
			self.get_config_data.get_error_base('getAvailableCoupon', [model, '优惠券列表', 'activity'], e)
		try:
			self.activity.recharge_list([model, '充值活动列表', 'shop'])
		except Exception as e:
			self.get_config_data.get_error_base('getRechargeList', [model, '充值活动列表', 'shop'], e)
		try:
			self.user.init_shop([model, '会员初始化', 'user'])
		except Exception as e:
			self.get_config_data.get_error_base('initUserShop', [model, '会员初始化', 'user'], e)

	# 支付完成
	def pay_success(self):
		model = ["订单", "支付完成", 'shop']
		try:
			self.shop.detail(model)
		except Exception as e:
			self.get_config_data.get_error_base('shopDetail', model, e)
		model = ["订单", "支付完成", 'goods']
		try:
			self.goods.check(model)
		except Exception as e:
			self.get_config_data.get_error_base('checkGoodsStatusList', model, e)
		model = ["订单", "支付完成", 'order']
		try:
			self.order.detail(model)
		except Exception as e:
			self.get_config_data.get_error_base('orderDetail', model, e)
		model = ["订单", "支付完成", 'activity']
		try:
			self.coupon.coupon_get_share(model)
		except Exception as e:
			self.get_config_data.get_error_base('getShareCoupon', model, e)
		try:
			self.coupon.check_invite_conf(model)
		except Exception as e:
			self.get_config_data.get_error_base('isCashBack', model, e)
		try:
			self.coupon.coupon_goods_able_list(model)
		except Exception as e:
			self.get_config_data.get_error_base('getCouponGoodsList', model, e)

	# 广告位
	def poster(self):
		model = ["广告", "广告位", 'goods']
		try:
			self.goods.advertising_list(model)
		except Exception as e:
			self.get_config_data.get_error_base('getAdListData', model, e)
		try:
			self.coupon.get_reg(model)
		except Exception as e:
			self.get_config_data.get_error_base('getRegConfigInfo', model, e)


if __name__ == '__main__':
	run = Goods()
# run.my_data()
# run.my_order()
# run.add_order()
