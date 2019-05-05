from lib.client import RunMethod


class SendPost:

	def send_post(self, url, data, header = None):
		run = RunMethod()
		ret = run.request_post(url, data, header)
		ret['report_status'] = ret['status']
		ret['report_base_status'] = ret['status']
		return ret


if __name__ == '__main__':
	pass
# run = SendPost()
# run.send_post('http://www.baidu.com', "", "")
