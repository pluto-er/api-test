import time
from lib.client import RunMethod
from lib.global_val import glo

corpid = "wwf9c376064d78d25f"  # 企业id
corpsecret = "dbj5tOQcTqB3z2F6rKjPMDl84fxMAUqmZ6Z2d23ZyBo"  # 密钥


class Qywx:

	def get_access_token(self):
		access_token = glo.get_value('access_token')
		access_token_time = glo.get_value('access_token_time')
		if not access_token_time or access_token_time >= time.time():
			url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corpid + "&corpsecret=" + corpsecret
			run = RunMethod()
			ret = run.request_get(url)
			glo.set_value('access_token', ret['access_token'])
			end_time = int(time.time()) + ret['expires_in']
			glo.set_value('access_token_time', end_time)
			access_token = ret['access_token']

		return access_token

	def send_msg_qywx_text(self, data):
		access_token = self.get_access_token()
		post_data = {
			"touser": data['touser'],
			"totag": data['totag'],
			"toparty": data['toparty'],  # 三选一
			"msgtype": "text",
			"agentid": data['agentid'],
			"text": {
				"content": data['content']
				},
			"safe": 0
			}
		url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + str(access_token)
		run = RunMethod()
		run.post(url, post_data)
		return True


if __name__ == '__main__':
	run = Qywx()
	run.send_msg_qywx_text({'touser': '', "totag": "", "toparty": "2|4", "agentid": 1000012, "content": ""})
