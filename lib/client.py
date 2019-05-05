# coding:utf-8
import requests
import urllib3

urllib3.disable_warnings()
import json
import time
from helper.send_email import SendEmailHelper


class RunMethod:

	def request_post(self, url, data, header = None):
		res = None
		start_time = int(time.time() * 1000)
		if header != None:
			try:
				res = requests.post(url = url, data = json.dumps(data), headers = header)
			except Exception as e:
				SendEmailHelper().send_report_email('测试Api执行错误', str(e))
		else:
			res = requests.post(url = url, data = data)
		end_time = int(time.time() * 1000)
		ret = res.json()
		ret_header = res.headers
		ret['request_time'] = end_time - start_time
		if "X-Request-Id" in ret_header:
			ret['traceid'] = ret_header['X-Request-Id']
		else:
			ret['traceid'] = ""

		return ret

	def request_get(self, url, data = None, header = None):
		res = None
		if header != None:
			res = requests.get(url = url, data = data, headers = header, verify = False)
		else:
			res = requests.get(url = url, data = data, verify = False)
		return res.json()

	def post(self, url, data):
		res = requests.post(url, json.dumps(data))
		return res
