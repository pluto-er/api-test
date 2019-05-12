# coding:utf-8
import sys
import os
import random
import time

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from helper.get_yaml import GetYaml
from helper.get_html import GetHtml
from helper.request_post import SendPost
from helper.validator import ValidatorHelper
from helper.get_premise import GetPremise
from helper.get_config import GetDataConfig
from data.orderdata import OrderData


class CommentData:

	def __init__(self):
		self.comment_list_data = GetYaml()
		self.get_html_data = GetHtml()
		self.get_yaml_data = GetYaml()
		self.comment_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_data_config = GetDataConfig()
		self.order = OrderData()
		self.get_premise = GetPremise()

	# 获取评论列表
	def list(self, model = [], post_data = None):
		file_path = "/public/yaml/comment/list.yaml"
		ret = self.get_data_config.get_data_post("commentList", file_path)
		url = ret['url']
		header = ret['header']
		if post_data is None:
			post_data = ret['expect']['retData']

		# 循环用例，请求获取数据
		for data in post_data:
			total = 0
			cases_text = data['cases_text']
			page_text = {1: "", 0: "第0页", 100: "最后一页", 101: "大于最后一页"}
			for page_post in [1, 0, 100, 101]:
				data['page'] = page_post
				page_data = self.validator.set_page(data, total)
				data['page'] = page_data['page']
				page_size = page_data['page_size']

				params = self.comment_post.send_post(url, data, header)
				result_status = self.validator.validate_status(ret, params, model, data)
				if result_status == 'fail':
					continue

				# 特殊值断言
				report = ""
				if params['data']['star'] > 500 or params['data']['star'] < 0:
					params['report_status'] = 204
					report += "评论总评分错误;star=" + str(params['data']['star']) + "<br/>"

				if params['data']['list']:
					total = params['data']['total']
					report += self.validator.page(page_size, params['data']['total'], params['data']['list'], data)

					for list_data in params['data']['list']:
						# 断言星数是否对应
						if int(list_data['orderStar']) != int(data['star']):
							params['report_status'] = 204
							report += "评论星级筛选错误;orderno=" + str(list_data['orderno']) + "结果星级;star=" + str(
									list_data['orderStar']) + "<br/>"
						# 断言类型
						if int(list_data['type']) != int(data['type']):
							if (list_data['type'] == 2 and data['type'] == 1) or (
									list_data['type'] == 5 and data['type'] == 4):
								pass
							else:
								params['report_status'] = 204
								report += "评论类型筛选错误;orderno=" + str(list_data['orderno']) + "结果类型;type=" + str(
										list_data['type']) + "<br/>"
						# 断言内容
						if not list_data['content']:
							params['report_status'] = 202
							report += "评论内容筛选错误;orderno=" + str(list_data['orderno']) + "结果为空<br/>"
						# 断言回复
						if list_data['replay']:
							for replay_data in list_data['replay']:
								if replay_data['cid'] != list_data['id']:
									params['report_status'] = 204
									report += "评论回复内容错误;列出了不属于cid=" + str(list_data['id']) + "的评论,replay_cid=" + str(
											replay_data[
												'cid']) + "<br/>"
								if not replay_data['fromName']:
									params['report_status'] = 202
									report += "回复者名称为空;评论cid=" + str(replay_data['cid']) + \
											  ";replay_id=" + str(replay_data['id']) + ";name=" + str(
											replay_data['fromName']) + "<br/>"
								if not replay_data['toName']:
									params['report_status'] = 202
									report += "被回复者名称为空;评论id=" + str(replay_data['cid']) + ",replay_id=" + str(
											replay_data[
												'id']) + "<br/>"
								if not replay_data['content']:
									params['report_status'] = 202
									report += "回复内容为空;评论id=" + str(replay_data['cid']) + ",replay_id=" + str(
											replay_data[
												'id']) + "<br/>"

				else:
					report += "没有评论数据"
				result_status['report'] = report
				data['cases_text'] = page_text[page_post] + cases_text
				self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 点赞/取消点赞
	def add_like(self, model):
		file_path = "/public/yaml/comment/add_like.yaml"
		ret = self.get_data_config.get_data_post("changeLike", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']
		# 获取评论列表
		comment_post_data = [
			{"type": random.choice([1, 3, 4]), "star": random.randint(1, 5), "page": 1, "size": 5, "state": 1}]
		comment_return = self.get_premise.get_comment_list(comment_post_data)
		comment = comment_return['data']
		if not comment['data']['list']:
			comment['report_status'] = 202
			comment['message'] = "没有评论"
			result_status = {"key": [], "val": [], 'report': ""}
			self.get_yaml_data.set_to_yaml(ret, comment_return['post'], comment, model, result_status)
			return False

		for comment_data in comment['data']['list']:
			if comment_data['isLike'] == 1:
				continue
			choice_comment = comment_data
			break

		# 循环用例，请求获取数据
		for data in post_data:
			data['cid'] = choice_comment['id']
			like = len(choice_comment['likeList'])
			params = self.comment_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)
			if result_status == 'fail':
				continue

			# 断言是否写入成功
			detail = self.comment_detail_condition(data['cid'])
			like_num = len(detail['data']['comment']['likeList'])
			if like_num == like:
				params['report_status'] = 204
				result_status['report'] = "点赞/点踩失败,type=" + str(data['type'])
				self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 发布回复
	def add_replay(self, model):
		file_path = "/public/yaml/comment/add_replay.yaml"
		ret = self.get_data_config.get_data_post("addReplay", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']

		# 获取评论列表
		comment_post_data = [
			{"type": random.choice([1, 3, 4]), "star": random.randint(1, 5), "page": 1, "size": 5, "state": 1}]
		comment_return = self.get_premise.get_comment_list(comment_post_data)
		comment = comment_return['data']
		if not comment['data']['list']:
			comment['report_status'] = 202
			comment['message'] = "没有评论"
			result_status = {"key": [], "val": [], 'report': ""}
			self.get_yaml_data.set_to_yaml(ret, comment_return['post'], comment, model, result_status)
			return False
		comment_data = random.choice(comment['data']['list'])
		# 循环用例，请求获取数据
		for data in post_data:
			# 评论评论
			data['cid'] = comment_data['id']
			data['toId'] = comment_data['uid']

			params = self.comment_post.send_post(url, data, header)
			if not data['content']:
				result_status = {"key": [], "val": [], 'report': "无评论信息，已手动屏蔽错误"}
				params['status'] = 200
				params['message'] = ''
				self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)
				continue
			result_status = self.validator.validate_status(ret, params, model, data)
			if result_status == "fail":
				continue

			# 断言是否写入成功
			detail = self.comment_detail_condition(data['cid'])
			replay = detail['data']['replay']
			# 断言回复评论
			if int(replay[len(replay) - 1]['fromId']) != int(header['uid']):
				params['report_status'] = 204
				result_status['report'] = "发布评论失败"
				self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)
				continue

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

			# 评论回复
			comment_replay = random.choice(comment['data']['list'])
			if comment_replay['replay']:
				data['cases_text'] = "回复评论的评论"
				replay_post = random.choice(comment_replay['replay'])
				data['cid'] = comment_replay['id']
				data['toId'] = replay_post['fromId']
				data['toType'] = replay_post['fromType']
				data['replayId'] = replay_post['id']
				params = self.comment_post.send_post(url, data, header)
				result_status = self.validator.validate_status(ret, params, model, data)
				if result_status == "fail":
					continue

				# 断言是否写入成功
				detail = self.comment_detail_condition(data['cid'])
				replay = detail['data']['replay']
				if int(replay[len(replay) - 1]['fromId']) != int(header['uid']):
					params['report_status'] = 204
					result_status['report'] = "发布评论失败"
					self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)
					continue

				self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# =====================================
	# 新增评论
	def add_comment(self, model):
		file_path = "/public/yaml/comment/add_comment.yaml"
		ret = self.get_data_config.get_data_post("addOrderComment", file_path)
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']
		# 循环用例，请求获取数据
		for star in [1, 2, 3, 4, 5]:
			if star == 1:
				star_text = "【一星差评】"
			elif star == 2:
				star_text = "【二星差评】"
			elif star == 3:
				star_text = "【三星中评】"
			elif star == 4:
				star_text = "【四星中评】"
			else:
				star_text = "【五星好评】"

			for data in post_data:
				# 获取订单
				order_list = self.order.list(model, [{"status": [8]}])
				if order_list['data']['list']:
					order_one = random.choice(order_list['data']['list'])
				else:
					result_status = {"key": [], "val": [], 'report': "没有未评论订单"}
					data['cases_text'] = star_text + data['cases_text']
					self.get_yaml_data.set_to_yaml(ret, data, order_list, model, result_status)
					break
				# 请求api获取结果
				data['orderId'] = order_one['id']
				data['orderno'] = order_one['orderno']
				data['orderStar'] = star
				data['goodsStar'] = random.randint(1, 5)
				data['serviceStar'] = random.randint(1, 5)
				data['environmentStar'] = random.randint(1, 5)
				data['type'] = order_one['type']
				data['goods'] = []
				for goods_data in order_one['goodsList']:
					goods = {"goodsId": goods_data['goodsId'], 'goodsName': goods_data['goodsName'],
						'type': random.randint(1, 2)}
					data['goods'].append(goods)
				data['content'] = "自动测试评论，时间：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
				# 标签
				type = data['type']
				if data['type'] == 4:
					type = 1
				elif data['type'] == 5:
					type = 2
				ret_label = self.get_label_list(model, [{"type": type}])
				data['label'] = []
				if ret_label['data']:
					if data['orderStar'] in [1, 2]:
						ret_label_data = ret_label['data']['bad']
					else:
						ret_label_data = ret_label['data']['good']
					for choice in ret_label_data:
						label = {"labelId": choice['id'], "labelName": choice['title'], "labelType": choice['type']}
						data['label'].append(label)
				params = self.comment_post.send_post(url, data, header)
				result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
				if result_status == 'fail':
					continue

				data['cases_text'] = star_text + data['cases_text']
				self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return True

	# 删除
	def delete(self):
		result = 200
		# 获取文件请求数据
		file_path = "/public/yaml/comment/delete.yaml"
		ret = self.get_data_config.get_data_post("delComment", file_path)

		# 组装请求数据
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']
		ret_result = []

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			params = self.comment_post.send_post(url, data, header)

			# 判断status
			result_status = self.validator.validate_status(ret['expect'], params)
			if result_status == 'fail':
				result = 500
			data['result_data'] = result_status
			data['result_value'] = ''
			ret_result.append(data)

			# 写入html
			msg = params['message']
			self.get_html_data.set_html(url, result_status, data, '评论', msg)

		# 写入结果yaml
		file_request_path = "/public/yaml/comment/delete_request.yaml"
		self.comment_list_data.set_to_yaml(file_request_path, ret_result)

		return result

	# 删除回复
	def delete_replay(self):
		result = 200
		# 获取文件请求数据
		file_path = "/public/yaml/comment/delete_replay.yaml"
		ret = self.get_data_config.get_data_post(file_path)

		# 组装请求数据
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']
		ret_result = []

		# 循环用例，请求获取数据
		for data in post_data:
			# 请求api获取结果
			params = self.comment_post.send_post(url, data, header)

			# 判断status
			result_status = self.validator.validate_status(ret['expect'], params)
			if result_status == 'fail':
				result = 500

			data['result_data'] = result_status
			data['result_value'] = ''
			ret_result.append(data)
			# 写入html
			msg = params['message']
			self.get_html_data.set_html(url, result_status, data, '评论', msg)
		# 写入结果yaml
		file_request_path = "/public/yaml/comment/delete_replay_request.yaml"
		self.comment_list_data.set_to_yaml(file_request_path, ret_result)

		return result

	# 获取详情
	def get_detail(self):
		result = 200
		# 获取文件请求数据
		file_path = "/public/yaml/comment/get_detail.yaml"
		ret = self.get_data_config.get_data_post("getCommentDetail", file_path)

		# 组装请求数据
		url = ret['url']
		header = ret['header']
		post_data = ret['expect']['retData']
		ret_result = []

		for data in post_data:
			params = self.comment_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret['expect'], params)
			if result_status == 'fail':
				result = 500

			data['result_data'] = result_status
			data['result_value'] = ''
			ret_result.append(data)

			# 写入html
			msg = params['message']
			self.get_html_data.set_html(url, result_status, data, '评论', msg)
		# 写入结果yaml
		file_request_path = "/public/yaml/comment/get_detail_request.yaml"
		self.comment_list_data.set_to_yaml(file_request_path, ret_result)
		return result

	# 获取标签列表
	def get_label_list(self, model, post_data = None):
		file_path = "/public/yaml/comment/get_label_list.yaml"
		ret = self.get_data_config.get_data_post("getOrderCommentTags", file_path)
		url = ret['url']
		header = ret['header']
		if not post_data:
			post_data = ret['expect']['retData']
		for data in post_data:
			params = self.comment_post.send_post(url, data, header)
			result_status = self.validator.validate_status(ret, params, model, data)  # 判断status
			if result_status == 'fail':
				result = 500

			self.get_yaml_data.set_to_yaml(ret, data, params, model, result_status)

		return params

	# 获取前提评论列表
	def comment_list_condition(self):
		config = self.get_data_config.get_conf("commentList")
		# 组装请求数据
		url = config['host'] + config['uri']
		header = config['header']
		data = {"type": 1, "star": 5, "page": 1, "size": 10, "state": 1}
		# 请求api获取结果
		params = self.comment_post.send_post(url, data, header)

		return params

	# 根据cid获取评论详情
	def comment_detail_condition(self, cid):
		config = self.get_data_config.get_conf("getCommentDetail")
		# 组装请求数据
		url = config['host'] + config['uri']
		header = config['header']
		data = {"type": 1, "targetId": cid}
		# 请求api获取结果
		params = self.comment_post.send_post(url, data, header)

		return params

	def get_comment_list(self, model, data):
		comment = self.list(model, data)
		if not comment['data']['list']:
			comment_post_data = [
				{"type": random.choice([1, 3, 4]), "star": random.randint(1, 5), "page": 1, "size": 5, "state": 1}]
			self.get_comment_list(model, comment_post_data)
		result = {"data": comment, "post": data}
		return result


if __name__ == '__main__':
	run = CommentData()
	ret = run.add_comment(['评论', '新增'])
	print(ret)
