import operator
from helper.get_html import GetHtml
from helper.get_yaml import GetYaml


class ValidatorHelper:
	def __init__(self):
		self.get_html_data = GetHtml()
		self.get_yaml_data = GetYaml()

	# 验证固定值
	def validate_status(self, expect, params, model, data, todo = True):
		if not params:
			result_status = {"key": [], "val": [], 'report': ""}
			params = {"report_status": 500, "request_time": 0, "traceid": "", "status": 500,
				"message": "服务器没有返回任何值，包括status", "code": 0}
			self.get_yaml_data.set_to_yaml(expect, data, params, model, result_status)
			return 'fail'
		elif int(params['code']) == 0 and (int(expect['expect']['result']['status']) == int(params['status'])):
			if todo:
				ret = self.get_round_status(expect['expect']['result']['data'], params['data'], 0, [], [])
				ret['report'] = ''
				ret['key'] = list(set(ret['key']))
				ret['val'] = list(set(ret['val']))
				if ret['key'] or ret['val']:
					ret['report_base_status'] = 204
				return ret
			return {"key": [], "val": [], 'report': ""}
		else:
			result_status = {"key": [], "val": [], 'report': ""}
			self.get_yaml_data.set_to_yaml(expect, data, params, model, result_status)
			return 'fail'

	def get_round_status(self, expect, request, k = 0, flag_key = [], flag_value = [], skip_key = ['cityList', 'test'],
						 parent_key = ""):
		if k > 100:  # 防止死循环
			return {"key": flag_key, "val": flag_value}
		if not expect:
			return {"key": flag_key, "val": flag_value}
		if not request:
			return {"key": flag_key, "val": flag_value}
		if isinstance(expect, list):
			if not expect or not request:
				return {"key": flag_key, "val": flag_value}
			k = k + 1
			for data in request:
				if isinstance(expect, list) and (
						isinstance(expect[0], list) or isinstance(expect[0], dict)):
					self.get_round_status(expect[0], data, k, flag_key, flag_value, skip_key)
				else:
					continue
			return {"key": flag_key, "val": flag_value}
		keys1 = expect.keys()
		keys2 = request.keys()
		for key in keys1:
			if key not in keys2:
				flag_key.append(parent_key + '>' + key)
				continue
			if request[key] != 0 and type(expect[key]) != type(request[key]):
				flag_value.append(parent_key + '>' + key)
			# 判断类型
			if isinstance(expect[key], list):
				if not expect[key] or not request[key]:
					continue
				k = k + 1
				for data in request[key]:
					if isinstance(expect[key], list):
						if isinstance(expect[key][0], list) or isinstance(expect[key][0], dict):
							self.get_round_status(expect[key][0], data, k, flag_key, flag_value, skip_key, key)

			if isinstance(expect[key], dict):
				if not expect[key] or not request[key]:
					continue
				k = k + 1
				if isinstance(expect[key], dict):
					self.get_round_status(expect[key], request[key], k, flag_key, flag_value, skip_key, key)

		return {"key": flag_key, "val": flag_value}

	# 转换字典成数组
	def set_dict_list(self, data, params):
		data_val = []
		params_val = []
		data_key = data.keys()

		for data_key_data in data_key:
			data_val.append(data[data_key_data])

		params_key = params.keys()
		for params_key_data in params_key:
			params_val.append(params[params_key_data])
		return {"data": data_val, "params": params_val}
