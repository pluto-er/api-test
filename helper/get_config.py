# coding:utf-8
import sys

# sys.path.append('C:/Python/TEST/wzl-api-test')
from helper.get_yaml import GetYaml
from helper.request_post import SendPost
from helper.validator import ValidatorHelper
from helper.get_yaml import GetYaml


class GetDataConfig:

	def __init__(self):
		self.comment_list_data = GetYaml()
		self.comment_post = SendPost()
		self.validator = ValidatorHelper()
		self.get_yaml_data = GetYaml()

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
		url = host + uri
		result = {'host': host, 'header': header, 'uri': uri, 'url': url}
		return result

	def get_error_base(self, uri, model, e):
		ret = self.get_conf(uri)
		ret["expect"] = {"result": []}
		pay_ret = {'data': {}, 'status': 500, 'code': 0, 'message': "自动化程序报错:Exception=" + str(e),
			"request_time": 0, "traceid": 0}
		result_status = {"key": [], "val": [], 'report': ""}

		self.get_yaml_data.set_to_yaml(ret, {"cases_text": model[1]}, pay_ret, model, result_status)


if __name__ == '__main__':
	run = GetDataConfig()
	ret = run.get_url("loginUrl")
	print(ret)
