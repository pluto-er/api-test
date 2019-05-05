import time
import os
import sys

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录
sys.path.append(root_path)

from lib.operation_yaml import OperationYaml
from lib.global_val import glo
from helper.qywx import Qywx


# 获取yaml
class GetYaml:

	# 获取yaml数据
	@staticmethod
	def get_yaml(file_path):
		return OperationYaml.get(file_path)

	# 写入yaml数据 file_path地址   data新增数据
	@staticmethod
	def set_to_yaml(ret, data, params, model, result_code):
		file_path = "/public/report/" + glo.get_value('report_yaml') + "-header.yaml"
		file_data = OperationYaml.get(file_path)

		if "report_base_status" not in result_code:
			result_code['report_base_status'] = 200
		file_data['testAll'] = int(file_data['testAll']) + 1
		# 判断是否成功
		if params['status'] == 500:
			file_data['testError'] = int(file_data['testError']) + 1
			print(ret['uri'] + "     Error:msg=" + str(params['message']) + ";traceid=" + str(params['traceid']))
			status_code = "错误"
		elif result_code['report_base_status'] == 204:
			file_data['testFail'] = int(file_data['testFail']) + 1
			print(ret['uri'] + "     Fail:key=" + str(result_code['key']) + ":val=" + str(
					result_code['val']) + ":report=" + str(
					result_code['report']) + ";traceid=" + str(params['traceid']))
			status_code = "失败"
		elif params['report_status'] == 202:
			file_data['testSkip'] = int(file_data['testSkip']) + 1
			print(ret['uri'] + "     warning;msg" + str(result_code['report']))
			status_code = "警告"
		elif params['status'] == 200 and params['code'] == 0:
			print(ret['uri'] + "     success")
			file_data['testPass'] = int(file_data['testPass']) + 1
			status_code = "成功"
		else:
			file_data['testFail'] = int(file_data['testFail']) + 1
			print(ret['uri'] + "     warning;msg" + str(params['message']))
			status_code = "失败"
		# 判断是否存在用例
		try:
			if ret['expect']['test_cases']:
				test_cases = "<a target='view_window' href='" + str(ret['expect']['test_cases']) + "'>关联用例</a>"
			else:
				test_cases = "无"
		except KeyError:
			test_cases = "无"

		# 断言结果值
		if not result_code['key']:
			result_code['key'] = "无"
		if not result_code['val']:
			result_code['val'] = "无"
		if not result_code['report']:
			result_code['report'] = "无"
		# 组装数据
		result = [
			{
				"className": model[0],
				"modelName": model[1],
				"methodName": ret['uri'],
				"description": str(data),
				"spendTime": params['request_time'],
				"status": status_code,
				"traceid": params['traceid'],
				"log": [
					"bid=" + str(ret['header']['bid']) + ";sid=" + str(ret['header']['sid']) + ";uid=" + str(
							ret['header']['uid']),
					ret['host'],
					params['status'],
					params['code'],
					params['message'],
					[result_code['key']],
					[result_code['val']],
					result_code['report'],
					time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
					test_cases,
					str(ret['expect']['result']),
					str(params),
					]
				},
			]
		# if status_code in ['错误', '失败']:
		# 	send_data = "【" + str(model[0]) + "-" + str(model[1]) + "】出错 traceid=" + str(
		# 			params['traceid']) + "，message=" + str(params['message']) + ",report=" + str(result_code['report']) \
		# 				+ ",缺少key=" + str([result_code['key']]) + ",value值错误=" + str([result_code['val']]) + \
		# 				",url=" + str(ret['url']) + ",\nexpect=" + str(ret['expect']['result']) + "，\nresult=" + str(
		# 			params)
		# 	qywx = Qywx()
		# 	qywx.send_msg_qywx_text(
		# 			{'touser': 'plutoer', "totag": "", "toparty": "", "agentid": 1000012, "content": send_data})
		# 写入base
		OperationYaml.set(file_path, file_data)

		# 追加数据到对应的yaml
		file_path = "/public/report/" + glo.get_value('report_yaml') + ".yaml"
		OperationYaml.add(file_path, result)

	# 获取yaml数据
	@staticmethod
	def get_config():
		return OperationYaml.get_config()

	@staticmethod
	def init_file(file_name):
		# 获取基础配置
		conf = OperationYaml.get('/public/report/base.yaml')
		conf['beginTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		conf['begin_time'] = time.time()

		# 判断是否存在路径
		day = time.strftime('%Y%m%d', time.localtime(time.time()))
		first_file_path = root_path + "/public/report/" + day
		is_exists = os.path.exists(first_file_path)
		if not is_exists:
			os.makedirs(first_file_path)

		# 判断是否存在路径
		first_file_path = root_path + "/public/html/" + day
		is_exists = os.path.exists(first_file_path)
		if not is_exists:
			os.makedirs(first_file_path)

		# 创建yaml数据
		file_path = "/public/report/" + day + "/" + file_name + "-header.yaml"
		OperationYaml.create(file_path, conf)

		glo.set_value('report_yaml', day + "/" + file_name)
		return file_path

	@staticmethod
	def init_file_test(file_path):
		# 获取基础配置
		conf = OperationYaml.get('/public/report/base.yaml')
		conf['beginTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		conf['begin_time'] = time.time()

		OperationYaml.create(file_path, conf)
