#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 链接数据库
import MySQLdb


class OperationDb:
	@staticmethod
	def select(data, sql):
		# 打开数据库连接
		db = MySQLdb.connect("118.24.141.135", 'root', 'password', data, charset = 'utf8mb4')

		# 使用cursor()方法获取操作游标
		cursor = db.cursor()

		# SQL 插入语句
		try:
			# 执行sql语句
			cursor.execute(sql)
			# 提交到数据库执行
			results = cursor.fetchall()

		except  Exception as e:
			print(e)
			# 发生错误时回滚
			return []

		# 关闭数据库连接
		db.close()
		return results
