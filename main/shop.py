import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from data.shopdata import ShopData
from data.workerdata import WorkerData
from data.commentdata import CommentData
from data.goodsdata import GoodsData
from data.msgdata import MsgData
from helper.get_config import GetDataConfig


class Shop:

	def __init__(self):
		self.shop = ShopData()
		self.worker = WorkerData()
		self.goods = GoodsData()
		self.comment = CommentData()
		self.msg = MsgData()
		self.get_config_data = GetDataConfig()

	# 整个商铺模块
	def start_up(self):
		model = '店铺'
		try:
			self.worker.list([model, '为你服务'])
		except Exception as e:
			self.get_config_data.get_error_base('workerList', [model, '为你服务'], e)
		try:
			self.shop.reward_set([model, '为你服务'])
		except Exception as e:
			self.get_config_data.get_error_base('getRewardSet', [model, '为你服务'], e)
		try:
			self.worker.reward_pay([model, '为你服务'])
		except Exception as e:
			self.get_config_data.get_error_base('getRewardSet', [model, '为你服务'], e)
		try:
			self.worker.evaluation([model, '为你服务'])
		except Exception as e:
			self.get_config_data.get_error_base('workerEvaluation', [model, '为你服务'], e)
		# 评论模块
		try:
			self.comment.list([model, '评论列表'])
		except Exception as e:
			self.get_config_data.get_error_base('commentList', [model, '评论列表'], e)
		try:
			self.comment.add_like([model, '评论列表'])
		except Exception as e:
			self.get_config_data.get_error_base('changeLike', [model, '评论列表'], e)
		try:
			self.comment.add_replay([model, '评论列表'])
		except Exception as e:
			self.get_config_data.get_error_base('addReplay', [model, '评论列表'], e)
		# 店铺相关
		try:
			self.shop.detail([model, '店铺相关'])
		except Exception as e:
			self.get_config_data.get_error_base('shopDetail', [model, '店铺相关'], e)
		try:
			self.shop.story_detail([model, '店铺相关'])
		except Exception as e:
			self.get_config_data.get_error_base('storyDetail', [model, '店铺相关'], e)
		# 菜品推荐
		try:
			self.goods.config([model, '菜品推荐'])
		except Exception as e:
			self.get_config_data.get_error_base('foodsConfigInfo', [model, '菜品推荐'], e)
		try:
			self.goods.recommend_list([model, '菜品推荐'])
		except Exception as e:
			self.get_config_data.get_error_base('recommendList', [model, '菜品推荐'], e)
		try:
			self.goods.recommend_one([model, '菜品推荐'])
		except Exception as e:
			self.get_config_data.get_error_base('recommendDetail', [model, '菜品推荐'], e)
		# 聊天
		try:
			self.msg.im_user_info([model, '有事找我'])
		except Exception as e:
			self.get_config_data.get_error_base('getIMUserInfo', [model, '有事找我'], e)
		try:
			self.msg.im_list([model, '有事找我'])
		except Exception as e:
			self.get_config_data.get_error_base('getOldIMMsg', [model, '有事找我'], e)


if __name__ == '__main__':
	run = Shop()
	run.start_up()
