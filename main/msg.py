import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from data.commentdata import CommentData
from data.msgdata import MsgData
from helper.get_config import GetDataConfig


class Msg:

	def __init__(self):
		self.msg = MsgData()
		self.comment = CommentData()
		self.get_config_data = GetDataConfig()

	# 消息模块
	def start_up(self):
		model = "用户"
		try:
			self.msg.detail([model, '消息计数', 'msg'])
		except Exception as e:
			self.get_config_data.get_error_base('getMessageCount', [model, '消息计数', 'msg'], e)
		try:
			self.msg.list([model, '消息通知列表', 'msg'])
		except Exception as e:
			self.get_config_data.get_error_base('getMessageList', [model, '消息通知列表', 'msg'], e)
		try:
			self.comment.add_replay([model, '回复评论', 'comment'])
		except Exception as e:
			self.get_config_data.get_error_base('addReplay', [model, '回复评论', 'comment'], e)
		try:
			self.msg.delete([model, '删除消息', 'msg'])
		except Exception as e:
			self.get_config_data.get_error_base('delMessage', [model, '删除消息', 'msg'], e)


if __name__ == '__main__':
	run = Msg()
	run.start_up()
