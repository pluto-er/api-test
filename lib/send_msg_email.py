# coding:utf-8
# 发送邮件

import smtplib
import os
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart


class SendEmail:

	def __init__(self, file_name = None, user_email = None, title = None, content = None):
		self.file_name = file_name  # 文件地址
		self.user_email = user_email  # 发送对象邮箱
		self.title = title  # 文件标题
		self.content = content  # 文件内容

	def send(self, user_email, title, content):
		my_sender = '1111111111@qq.com'  # 发件人邮箱账号
		my_pass = '1111111111'  # 发件人邮箱密码
		my_user = user_email  # 收件人邮箱账号，我这边发送给自己
		ret = True
		try:
			msg = MIMEMultipart()
			msg['From'] = formataddr(["FromRunoob", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
			msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
			msg['Subject'] = title  # 邮件的主题，也可以说是标题

			# 邮件正文内容
			msg.attach(MIMEText(content, 'html', 'utf-8'))

			server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
			server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
			server.sendmail(my_sender, [my_user], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
			server.quit()  # 关闭连接
		except Exception as e:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
			ret = False
			print(e)
		if ret:
			print("邮件发送成功")
		else:
			print("邮件发送失败")


if __name__ == "__main__":
	run = SendEmail()
	run.send()
