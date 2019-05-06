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
from data.workerdata import WorkerData
from helper.get_html import GetHtml


class User:

	def __init__(self):
		self.get_html_data = GetHtml()
		self.msg = MsgData()
		self.comment = CommentData()
		self.coupon = CouponData()
		self.activity = ActivityData()
		self.user = UserData()
		self.invitations = InvitationsData()
		self.user_comment = UserCommentData()
		self.order = OrderData()
		self.worker = WorkerData()

	# 用户页面
	def my_data(self):
		model = "我的"
		self.activity.recharge_list([model, '充值活动'])
		self.msg.push_count([model, '未读消极计数'])
		self.user.vip_data([model, '会员数据获取'])
		self.coupon.coupon_center([model, '领券中心'])
		self.user.info([model, '用户详情'])
		self.coupon.coupon_get_invite_rebate([model, '邀请比例'])

	# 我的优惠券
	def my_coupon(self):
		model = "优惠券"
		self.coupon.coupon_list([model, '优惠券列表'])
		self.user.star_sign([model, '星座'])
		self.coupon.coupon_used_amount([model, '使用总计'])
		self.coupon.coupon_get_share([model, '分享优惠券地址'])
		self.coupon.coupon_donate([model, '赠送好友'])
		# 领取红包
		self.coupon.get_share_coupon([model, '分享地址'])

	# 充值
	def my_recharge(self):
		model = "充值"
		self.user.recharge([model, '充值明细'])
		self.user.spending([model, '消费明细'])
		self.user.recharge_amount([model, '充值统计数据'])
		self.user.vip_recharge([model, '充值'])
		self.user.balance([model, '我的钱包'])
		self.user.code_receive([model, '注册'])

	# 邀请奖励
	def my_invitations(self):
		model = "邀请奖励"
		self.invitations.invitations_amount([model, '邀请奖励统计'])
		self.invitations.invitations_by_count([model, '消费人数统计'])
		self.invitations.invitations([model, '邀请奖励明细'])
		self.user.give([model, '赠送列表'])
		self.invitations.invitations_by([model, '邀请奖励明细'])
		self.coupon.coupon_invitations_rule([model, '邀请奖励规则'])
		self.coupon.get_invitations([model, '邀请优惠券'])

	# 评论
	def my_comment(self):
		model = "评论"
		# self.comment.list([model, '评论列表'])
		self.comment.get_label_list(['评论', '标签列表'])
		self.comment.add_comment([model, '发布评论'])
		self.user_comment.comment_list([model, '用户评论列表'])
		self.user_comment.comment_amount([model, '评论总计'])
		self.user_comment.comment_user_count([model, '评论统计'])

	# 订单
	def my_order(self):
		model = "订单"
		self.coupon.check_invite_conf([model, '邀请奖励比例'])
		self.order.list([model, '订单列表'])
		self.order.count([model, '订单统计'])
		self.order.detail([model, '订单详情'])
		self.worker.list([model, '员工列表'])
		self.order.add([model, '下单'])

	# self.comment.add_comment(['评论', '发布评论'])

	def user_all(self):
		self.my_data()
		self.my_coupon()
		self.my_recharge()
		self.my_invitations()
		self.my_comment()
		self.my_order()


if __name__ == '__main__':
	run = User()
	run.user_all()
