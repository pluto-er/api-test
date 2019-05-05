# coding:utf-8
import sys

# sys.path.append('C:/Python/TEST/wzl-api-test')
from helper.get_yaml import GetYaml
from helper.request_post import SendPost
from helper.validator import ValidatorHelper


class GetDataConfig:

	def __init__(self):
		self.comment_list_data = GetYaml()
		self.comment_post = SendPost()
		self.validator = ValidatorHelper()

	# 获取请求/预期值参数
	def get_data_post(self, file_name, file_path):
		# 加载yaml文件
		expect = self.comment_list_data.get_yaml(file_path)
		# 加载配置
		header_yaml = self.comment_list_data.get_config()
		# 组装url
		url = header_yaml['host'] + header_yaml['uri'][file_name]
		# 获取请求头部
		header = header_yaml['header']
		# 组装返回值
		result = {
			'host': header_yaml['host'],
			'url': url,
			'uri': header_yaml['uri'][file_name],
			'header': header,
			'expect': expect
			}

		return result

	# 只获取头部信息
	def get_conf(self, file_name = None):
		# 获取配置
		header_yaml = self.comment_list_data.get_config()
		uri = ""
		if file_name:
			header_yaml = self.comment_list_data.get_config()
			uri = header_yaml['uri'][file_name]

		host = header_yaml['host']
		header = header_yaml['header']
		result = {'host': host, 'header': header, 'uri': uri}
		return result


if __name__ == '__main__':
	run = GetDataConfig()
	ret = run.get_url("loginUrl")
	print(ret)
