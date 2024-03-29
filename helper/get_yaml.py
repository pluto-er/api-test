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
		set_data = data.copy()
		file_path = "/generate/report/" + glo.get_value('report_yaml') + "-header.yaml"
		file_data = OperationYaml.get(file_path)

		if "report_base_status" not in result_code:
			result_code['report_base_status'] = 200
		file_data['testAll'] = int(file_data['testAll']) + 1
		# 判断是否成功
		if params['status'] == 500 or params['report_status'] == 500 or params['code'] != 0:
			if not file_data['service']:
				file_data['service'][model[2]] = 1
			elif model[2] in file_data['service']:
				file_data['service'][model[2]] = file_data['service'][model[2]] + 1
			else:
				file_data['service'][model[2]] = 1
			file_data['testError'] = int(file_data['testError']) + 1
			print(ret['uri'] + "     Error:msg=" + str(params['message']) + ";traceid=" + str(params['traceid']))
			status_code = "错误"
		else:
			print(ret['uri'] + "     success")
			file_data['testPass'] = int(file_data['testPass']) + 1
			status_code = "成功"
		# elif result_code['report_base_status'] == 204:
		# 	file_data['testFail'] = int(file_data['testFail']) + 1
		# 	print(ret['uri'] + "     Fail:key=" + str(result_code['key']) + ":val=" + str(
		# 			result_code['val']) + ":report=" + str(
		# 			result_code['report']) + ";traceid=" + str(params['traceid']))
		# 	status_code = "失败"
		# elif params['report_status'] == 202:
		# 	if ret['uri'] != "/order/add":
		# 		file_data['testSkip'] = int(file_data['testSkip']) + 1
		# 		print(ret['uri'] + "     warning;msg" + str(result_code['report']))
		# 		status_code = "警告"
		# 	else:
		# 		file_data['testPass'] = int(file_data['testPass']) + 1
		# 		print(ret['uri'] + "      success")
		# 		status_code = "成功"
		# elif params['status'] == 200 and params['code'] == 0:
		# 	print(ret['uri'] + "     success")
		# 	file_data['testPass'] = int(file_data['testPass']) + 1
		# 	status_code = "成功"
		# else:
		# 	file_data['testFail'] = int(file_data['testFail']) + 1
		# 	print(ret['uri'] + "     warning;msg" + str(params['message']))
		# 	status_code = "失败"
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
			result_code['key'] = ""
		if not result_code['val']:
			result_code['val'] = ""
		if not result_code['report']:
			result_code['report'] = ""
		# 组装数据
		cases_text = set_data['cases_text']

		del set_data['cases_text']

		result = [
			{
				"className": model[0],
				"modelName": model[1],
				"service": model[2],
				"methodName": ret['uri'],
				"description": str(set_data),
				"caseText": str(cases_text),
				# "spendTime": params['request_time'],
				"status": status_code,
				"traceid": params['traceid'],
				"log": [
					"bid=" + str(ret['header']['bid']) + ";sid=" + str(ret['header']['sid']) + ";uid=" + str(
							ret['header']['uid']) + "<br/>POST=" + str(set_data),
					ret['host'] + "<br/>运行时长(毫秒)=" + str(params['request_time']),
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
		# 			params['traceid']) + "，message=" + str(params['message'])
		# 	if result_code['report'] != "无":
		# 		send_data += ",report=" + str(result_code['report'])
		# 	if result_code['key'] != "无":
		# 		send_data += ",缺少key=" + str([result_code['key']])
		# 	if result_code['val'] != "无":
		# 		send_data += ",value值错误=" + str([result_code['val']])
		# 	send_data += ",url=" + str(ret['url']) + ",\nexpect=" + str(ret['expect']['result']) + "，\nresult=" + str(
		# 			params)

		# 写入base
		OperationYaml.set(file_path, file_data)

		# 追加数据到对应的yaml
		file_path = "/generate/report/" + glo.get_value('report_yaml') + ".yaml"
		OperationYaml.add(file_path, result)

	# 初始化文件
	@staticmethod
	def init_file(file_name):
		# 获取基础配置
		conf = OperationYaml.get('/public/report/base.yaml')
		conf['beginTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
		conf['begin_time'] = time.time()

		# 判断是否存在路径
		day = time.strftime('%Y%m%d', time.localtime(time.time()))
		first_file_path = root_path + "/generate/report/" + day
		is_exists = os.path.exists(first_file_path)
		if not is_exists:
			os.makedirs(first_file_path)

		# 判断是否存在路径
		first_file_path = "/home/worker/wzl-api-qtp/www/" + day
		# first_file_path = root_path + "/generate/html/" + day
		is_exists = os.path.exists(first_file_path)
		if not is_exists:
			os.makedirs(first_file_path)

		# 创建yaml数据
		file_path = "/generate/report/" + day + "/" + file_name + "-header.yaml"
		OperationYaml.create(file_path, conf)

		glo.set_value('report_yaml', day + "/" + file_name)
		return file_path
