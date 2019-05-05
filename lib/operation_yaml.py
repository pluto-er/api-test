import yaml
import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 获取根目录


# 直接操作yaml文件
class OperationYaml:

	# 获取yaml文件内容
	@staticmethod
	def get(file_path):
		file_path = root_path + file_path
		f1 = open(file_path, 'r', encoding = 'utf-8')  # 打开yaml文件
		data = f1.read()  # 使用load方法加载
		data = yaml.full_load(data)
		return data

	# 设置yaml文件内容
	@staticmethod
	def set(file_path, data):
		file_path = root_path + file_path
		f2 = open(file_path, 'r', encoding = 'utf-8')  # 打开yaml文件
		old_data = f2.read()
		old_data = yaml.full_load(old_data)
		old_data['testResult'].append(data)
		f1 = open(file_path, 'w', encoding = 'utf-8')  # 写入yaml文件
		data = yaml.dump(data, f1)
		f1.close()
		f2.close()
		return data

	# 设置yaml文件内容
	@staticmethod
	def add(file_path, data):
		file_path = root_path + file_path
		f1 = open(file_path, 'a+', encoding = 'utf-8')  # 写入yaml文件
		ret = yaml.dump(data, f1)
		f1.close()
		return ret

	# 获取基础配置
	@staticmethod
	def get_config():
		file_path = root_path + '/config/config.yaml'
		f1 = open(file_path, 'r', encoding = 'utf-8')  # 打开yaml文件
		data = f1.read()  # 使用load方法加载
		data = yaml.full_load(data)
		return data

	# 创建yaml文件内容
	@staticmethod
	def create(file_path, data):
		file_path = root_path + file_path
		f1 = open(file_path, 'w', encoding = 'utf-8')  # 打开yaml文件
		yaml.dump(data, f1)
		f1.close()


if __name__ == '__main__':
	run = OperationYaml()
	ret = run.get('/public/yaml/shop/city_list.yaml')
	print(ret)
