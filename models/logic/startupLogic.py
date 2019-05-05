# coding:utf-8

import unittest
import HTMLTestRunner
import sys
import os

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 获取根目录
sys.path.append(root_path)

from models.data.shopdata import ShopData
from helper.send_email import SendEmailHelp
from helper.get_yaml import GetYaml


class StartupLogic(unittest.TestCase):

    def setUp(self):
        self.shopData = ShopData()

    # 获取评论列表
    def test_city_list(self):
        ret = self.shopData.list()
        self.assertEqual(ret, 200, 'no')

    # 点赞/取消赞
    def test_add_like(self):
        self.shopData.add_like()
        self.assertEqual(200, 200, 'no')

    # 发表回复
    def test_add_replay(self):
        self.shopData.add_replay()
        self.assertEqual(200, 200, 'no')

    # 发布评论
    def test_add_comment(self):
        self.shopData.add_comment()
        self.assertEqual(200, 200, 'no')

    # 获取详情
    def test_get_detail(self):
        self.shopData.get_detail()
        self.assertEqual(200, 200, 'no')

    # 获取标签
    def test_get_label_list(self):
        self.shopData.get_label_list()
        self.assertEqual(200, 200, 'no')

    # 删除回复
    def test_delete_replay(self):
        self.shopData.delete_replay()
        self.assertEqual(200, 200, 'no')

    # 删除评论
    def test_delete(self):
        self.shopData.delete()
        self.assertEqual(200, 200, 'no')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(StartupLogic('test_list'))
    suite.addTest(StartupLogic('test_add_like'))
    suite.addTest(StartupLogic('test_add_replay'))
    suite.addTest(StartupLogic('test_add_comment'))
    suite.addTest(StartupLogic('test_get_detail'))
    suite.addTest(StartupLogic('test_get_label_list'))
    suite.addTest(StartupLogic('test_delete_replay'))
    suite.addTest(StartupLogic('test_delete'))
    fp = open(root_path + "/public/report/comment_list.html", 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="评论测试报告", description='评论模块的所有报告')
    runner.run(suite)
    sendEmail = SendEmailHelp()
    get_yaml = GetYaml()

    # file_path = '../../public/yaml/html/comment.html'
    # title = "评论相关测试"
    # content = "这是一个评论相关的测试"
    # sendEmail.send_report_email(file_path, title, content)
