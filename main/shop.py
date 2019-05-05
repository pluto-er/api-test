import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from data.shopdata import ShopData
from data.workerdata import WorkerData
from data.commentdata import CommentData
from data.goodsdata import GoodsData
from data.msgdata import MsgData
from helper.get_html import GetHtml


class Shop:

	def __init__(self):
		self.shop = ShopData()
		self.worker = WorkerData()
		self.goods = GoodsData()
		self.comment = CommentData()
		self.get_html_data = GetHtml()
		self.msg = MsgData()

	# 整个商铺模块
	def start_up(self):
		model = '店铺'
		self.worker.list(['为你服务', '员工列表'])
		self.shop.reward_set(['为你服务', '打赏配置'])
		self.worker.reward_pay(['为你服务', '打赏'])
		self.worker.evaluation(['为你服务', '点赞/点踩'])
		self.comment.list([model, '评论列表'])
		self.comment.add_like([model, '评论点赞'])
		self.comment.add_replay([model, '评论回复'])

		self.shop.detail([model, '店铺详情'])
		self.shop.story_detail([model, '品牌故事'])
		self.goods.config([model, '菜品相关配置'])
		self.goods.recommend_list([model, '菜品推荐'])
		self.goods.recommend_one([model, '菜品推荐详情'])
		# 聊天
		self.msg.im_user_info([model, '有事找我'])
		self.msg.im_list([model, '有事找我'])


if __name__ == '__main__':
	run = Shop()
	run.start_up()
