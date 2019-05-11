import time
import os
from lib.operation_html import OperationHtml
from lib.operation_yaml import OperationYaml
from helper.send_email import SendEmailHelper
from lib.global_val import glo
from helper.qywx import Qywx

class GetHtml:

	def __init__(self):
		self.get_data_html = OperationHtml()
		self.get_yaml = OperationYaml()
		self.send_email = SendEmailHelper()

	def set(self, file_path, add_data):
		return self.get_data_html.set(file_path, add_data)

	# 写入html文件
	def set_html(self):
		file_path = "/public/report/" + glo.get_value('report_yaml')
		# 获取头部
		file_path_header = file_path + "-header.yaml"
		ret_header = self.get_yaml.get(file_path_header)
		# 获取正文
		file_path_data = file_path + ".yaml"
		ret_data = self.get_yaml.get(file_path_data)
		ret_header['totalTime'] = format(float(int(time.time()) - int(ret_header['begin_time'])) / float(60), '.2f')
		ret_header['testResult'] = ret_data
		send_html = "var  resultData=" + str(ret_header)
		file_name = "/public/html/" + glo.get_value('report_yaml') + ".html"
		self.get_data_html.set2(file_name, send_html)
		# 发送邮件
		conf = OperationYaml.get_config()
		title = "小程序API测试"
		content = '<html><h3>全面测试小程序api:' \
				  '</h3><a href="' + conf['case_url'] + file_name + '" ' \
																	'style="font-size:18px">点击查看报告</a></html>'
		qywx = Qywx()
		qywx.send_msg_qywx_text(
				{'touser': 'plutoer', "totag": "", "toparty": "", "agentid": 1000012, "content": content})
		print(content)

		# self.send_email.send_report_email(title, content)

	def set_start(self, file_path):
		return self.get_data_html.set_start(file_path)


if __name__ == '__main__':
	run = GetHtml()
	run.set_html()
