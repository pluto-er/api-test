# coding:utf-8


class glo:

	def __init__(self):  # 初始化
		global _global_dict
		_global_dict = {}

	@staticmethod
	def set_value(key, value):
		_global_dict[key] = value

	@staticmethod
	def get_value(key, defValue = None):

		try:
			return _global_dict[key]
		except KeyError:
			return defValue
