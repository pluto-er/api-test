import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from data.commentdata import CommentData
from data.msgdata import MsgData


class Msg:

	def __init__(self):
		self.msg = MsgData()
		self.comment = CommentData()

	# 消息模块
	def start_up(self):
		model = "消息"
		self.msg.detail([model, '消息计数'])
		self.msg.list([model, '消息通知列表'])
		self.comment.add_replay([model, '回复评论'])
		self.msg.delete([model, '删除消息'])


if __name__ == '__main__':
	run = Msg()
	run.start_up()
