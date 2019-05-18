from lib.client import RunMethod


class SendPost:

	def send_post(self, url, data, header = None, k = 0):
		run = RunMethod()
		ret = run.request_post(url, data, header)
		if ret['status'] == 500 and 'cURL error 28' in ret['message']:
			k = k + 1
			if k < 3:
				self.send_post(url, data, header, k)
		ret['report_status'] = ret['status']
		ret['report_base_status'] = ret['status']
		return ret


if __name__ == '__main__':
	pass
	# run = SendPost()
	# run.send_post('http://www.baidu.com', "", "")
