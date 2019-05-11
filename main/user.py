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
from helper.get_config import GetDataConfig


class User:

	def __init__(self):
		self.msg = MsgData()
		self.comment = CommentData()
		self.coupon = CouponData()
		self.activity = ActivityData()
		self.user = UserData()
		self.invitations = InvitationsData()
		self.user_comment = UserCommentData()
		self.order = OrderData()
		self.worker = WorkerData()
		self.get_config_data = GetDataConfig()

	# 用户页面
	def my_user(self):
		model = ["我的", "用户页面"]
		try:
			self.activity.recharge_list(model)
		except Exception as e:
			self.get_config_data.get_error_base('getRechargeList', model, e)
		try:
			self.msg.push_count(model)
		except Exception as e:
			self.get_config_data.get_error_base('getUnMsgDataNumber', model, e)
		try:
			self.user.vip_data(model)
		except Exception as e:
			self.get_config_data.get_error_base('getVipLevel', model, e)
		try:
			self.coupon.coupon_center(model)
		except Exception as e:
			self.get_config_data.get_error_base('getCouponCenterList', model, e)
		try:
			self.user.info(model)
		except Exception as e:
			self.get_config_data.get_error_base('getUserInfo', model, e)
		try:
			self.coupon.coupon_get_invite_rebate(model)
		except Exception as e:
			self.get_config_data.get_error_base('getInviteRebate', model, e)

	# 我的优惠券
	def my_coupon(self):
		model = ["我的", '优惠券']
		try:
			self.coupon.coupon_list(model)
		except Exception as e:
			self.get_config_data.get_error_base('getMyCouponList', model, e)
		try:
			self.user.recharge(model)
		except Exception as e:
			self.get_config_data.get_error_base('getRechargeDetail', model, e)
		try:
			self.user.star_sign(model)
		except Exception as e:
			self.get_config_data.get_error_base('getStarSignList', model, e)
		try:
			self.coupon.coupon_get_share(model)
		except Exception as e:
			self.get_config_data.get_error_base('getShareCoupon', model, e)
		try:
			self.coupon.coupon_donate(model)
		except Exception as e:
			self.get_config_data.get_error_base('coupongiving', model, e)
		try:
			self.coupon.get_share_coupon(model)
		except Exception as e:
			self.get_config_data.get_error_base('getLuckyShare', model, e)

	# 充值
	def my_recharge(self):
		model = "充值"
		try:
			self.user.recharge([model, '充值明细'])
		except Exception as e:
			self.get_config_data.get_error_base('getRechargeDetail', [model, '充值明细'], e)
		try:
			self.user.spending([model, '消费明细'])
		except Exception as e:
			self.get_config_data.get_error_base('getSpendingInfo', [model, '消费明细'], e)
		try:
			self.user.recharge_amount([model, '充值统计数据'])
		except Exception as e:
			self.get_config_data.get_error_base('getRechargeCount', [model, '充值统计数据'], e)
		try:
			self.user.vip_recharge([model, '充值'])
		except Exception as e:
			self.get_config_data.get_error_base('postRecharge', [model, '充值'], e)
		try:
			self.user.balance([model, '我的钱包'])
		except Exception as e:
			self.get_config_data.get_error_base('getAccountBalance', [model, '我的钱包'], e)
		try:
			self.user.code_receive([model, '注册'])
		except Exception as e:
			self.get_config_data.get_error_base('getUserCode', [model, '注册'], e)

	# 邀请奖励
	def my_invitations(self):
		model = "邀请奖励"
		try:
			self.invitations.invitations_amount([model, '邀请奖励统计'])
		except Exception as e:
			self.get_config_data.get_error_base('getInvitationsAmount', [model, '邀请奖励统计'], e)
		try:
			self.invitations.invitations_by_count([model, '消费人数统计'])
		except Exception as e:
			self.get_config_data.get_error_base('handelInvitationsUser', [model, '消费人数统计'], e)
		try:
			self.invitations.invitations([model, '邀请奖励明细'])
		except Exception as e:
			self.get_config_data.get_error_base('getInvitationsDetail', [model, '邀请奖励明细'], e)
		try:
			self.user.give([model, '赠送列表'])
		except Exception as e:
			self.get_config_data.get_error_base('getUserGiveList', [model, '赠送列表'], e)
		try:
			self.invitations.invitations_by([model, '邀请奖励明细'])
		except Exception as e:
			self.get_config_data.get_error_base('getUserInvitations', [model, '邀请奖励明细'], e)
		try:
			self.coupon.coupon_invitations_rule([model, '邀请奖励规则'])
		except Exception as e:
			self.get_config_data.get_error_base('getInvitationsRule', [model, '邀请奖励规则'], e)
		try:
			self.coupon.get_invitations([model, '邀请优惠券'])
		except Exception as e:
			self.get_config_data.get_error_base('getInvitationsInfo', [model, '邀请优惠券'], e)

	# 订单
	def my_order(self):
		model = "订单"
		try:
			self.coupon.check_invite_conf([model, '邀请奖励比例'])
		except Exception as e:
			self.get_config_data.get_error_base('isCashBack', [model, '邀请奖励比例'], e)
		try:
			self.order.list([model, '订单列表'])
		except Exception as e:
			self.get_config_data.get_error_base('getOrderList', [model, '订单列表'], e)
		try:
			self.order.count([model, '订单统计'])
		except Exception as e:
			self.get_config_data.get_error_base('getOrderCount', [model, '订单统计'], e)
		try:
			self.order.detail([model, '订单详情'])
		except Exception as e:
			self.get_config_data.get_error_base('orderDetail', [model, '订单详情'], e)
		try:
			self.worker.list([model, '员工列表'])
		except Exception as e:
			self.get_config_data.get_error_base('workerList', [model, '员工列表'], e)

	# 评论
	def my_comment(self):
		model = "评论"
		try:
			self.comment.get_label_list(['评论', '标签列表'])
		except Exception as e:
			self.get_config_data.get_error_base('getOrderCommentTags', [model, '标签列表'], e)
		try:
			self.comment.add_comment([model, '发布评论'])
		except Exception as e:
			self.get_config_data.get_error_base('addOrderComment', [model, '发布评论'], e)
		try:
			self.user_comment.comment_list([model, '用户评论列表'])
		except Exception as e:
			self.get_config_data.get_error_base('commentsRewardList', [model, '用户评论列表'], e)
		try:
			self.user_comment.comment_amount([model, '评论总计'])
		except Exception as e:
			self.get_config_data.get_error_base('getCommentAmount', [model, '评论总计'], e)
		try:
			self.user_comment.comment_user_count([model, '评论统计'])
		except Exception as e:
			self.get_config_data.get_error_base('getCommentUserCount', [model, '评论统计'], e)


# self.comment.add_comment(['评论', '发布评论'])

# def user_all(self):
# 	self.my_data()
# 	self.my_coupon()
# 	self.my_recharge()
# 	self.my_invitations()
# 	self.my_comment()
# 	self.my_order()


if __name__ == '__main__':
	run = User()
	run.user_all()
