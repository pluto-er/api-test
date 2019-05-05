from lib.send_msg_email import SendEmail
from lib.operation_yaml import OperationYaml


class SendEmailHelper:

	def __init__(self):
		self.send_msg = SendEmail()
		self.get_yaml_data = OperationYaml()

	# 发送邮件
	# file_name 为文件绝对地址
	def send_report_email(self, title, content):
		config = self.get_yaml_data.get_config()
		user_email = config['user_email']
		self.send_msg.send_case(user_email, title, content)


if __name__ == '__main__':
	run = SendEmailHelper()
	run.send_report_email('小程序API测试',
						  '<html><h1>全面测试小程序api:</h1><a href="http://192.168.101.179/public/html/20190426/20190426225419-46.html">点击查看报告</a></html>')
