# coding:utf-8
import sys
import os

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 获取根目录
sys.path.append(root_path)

from helper.get_yaml import GetYaml
from helper.get_html import GetHtml
from helper.request_post import SendPost
from helper.validator import ValidatorHelper
from helper.get_config import GetDataConfig


class CommentData:

    def __init__(self):
        self.comment_list_data = GetYaml()
        self.get_html_data = GetHtml()
        self.comment_post = SendPost()
        self.validator = ValidatorHelper()
        self.get_data_config = GetDataConfig()

    # 获取评论列表
    def list(self):
        result = 200

        # 获取文件请求数据
        file_path = "/public/yaml/comment/coupon_list.yaml"
        ret = self.get_data_config.get_data_post(file_path)
        # 组装请求数据
        url = ret['url']
        header = ret['header']
        post_data = ret['expect']['retData']
        ret_result = []

        # 循环用例，请求获取数据
        for data in post_data:
            # 请求api获取结果
            params = self.comment_post.send_post(url, data, header)

            # 判断status
            result_status = self.validator.validate_status(ret['expect'], params)
            if result_status == 'fail':
                result = 500

            # 判断返回值的key和value
            result_value = self.validator.validate_key_val(ret['expect'], params)

            # 组装返回值
            data['result_data'] = result_status
            data['result_value'] = result_value
            ret_result.append(data)

            # 写入html
            msg = params['message']
            self.get_html_data.set_html(url, result_status, data, '评论', msg)

        # 写入结果yaml
        file_request_path = "/public/yaml/comment/list_request.yaml"
        self.comment_list_data.set_to_yaml(file_request_path, ret_result)

        return result

    # 点赞
    def add_like(self):
        result = 200
        # 获取文件请求数据
        file_path = "/public/yaml/comment/add_like.yaml"
        ret = self.get_data_config.get_data_post(file_path)

        # 组装请求数据
        url = ret['url']
        header = ret['header']
        post_data = ret['expect']['retData']
        ret_result = []

        # 循环用例，请求获取数据
        for data in post_data:
            # 请求api获取结果
            params = self.comment_post.send_post(url, data, header)

            # 判断status
            result_status = self.validator.validate_status(ret['expect'], params)
            if result_status == 'fail':
                result = 500

            data['result_data'] = result_status
            data['result_value'] = ''
            ret_result.append(data)

            # 写入html
            msg = params['message']
            self.get_html_data.set_html(url, result_status, data, '评论', msg)

        # 写入结果yaml
        file_request_path = "/public/yaml/comment/add_like_request.yaml"
        self.comment_list_data.set_to_yaml(file_request_path, ret_result)

        return result

    # 发布回复
    def add_replay(self):
        result = 200
        # 获取文件请求数据
        file_path = "/public/yaml/comment/add_replay.yaml"
        ret = self.get_data_config.get_data_post(file_path)

        # 组装请求数据
        url = ret['url']
        header = ret['header']
        post_data = ret['expect']['retData']
        ret_result = []

        # 循环用例，请求获取数据
        for data in post_data:
            # 请求api获取结果
            params = self.comment_post.send_post(url, data, header)

            # 判断status
            result_status = self.validator.validate_status(ret['expect'], params)
            if result_status == 'fail':
                result = 500

            data['result_data'] = result_status
            data['result_value'] = ''
            ret_result.append(data)

            # 写入html
            msg = params['message']
            self.get_html_data.set_html(url, result_status, data, '评论', msg)

        # 写入结果yaml
        file_request_path = "/public/yaml/comment/add_replay_request.yaml"
        self.comment_list_data.set_to_yaml(file_request_path, ret_result)

        return result

    # 新增评论
    def add_comment(self):
        result = 200
        # 获取文件请求数据
        file_path = "/public/yaml/comment/add_comment.yaml"
        ret = self.get_data_config.get_data_post(file_path)

        # 组装请求数据
        url = ret['url']
        header = ret['header']
        post_data = ret['expect']['retData']
        ret_result = []

        # 循环用例，请求获取数据
        for data in post_data:
            # 请求api获取结果
            params = self.comment_post.send_post(url, data, header)

            # 判断status
            result_status = self.validator.validate_status(ret['expect'], params)
            if result_status == 'fail':
                result = 500

            data['result_data'] = result_status
            data['result_value'] = ''
            ret_result.append(data)

            # 写入html
            msg = params['message']
            self.get_html_data.set_html(url, result_status, data, '评论', msg)

        # 写入结果yaml
        file_request_path = "/public/yaml/comment/add_comment_request.yaml"
        self.comment_list_data.set_to_yaml(file_request_path, ret_result)

        return result

    # 删除
    def delete(self):
        result = 200
        # 获取文件请求数据
        file_path = "/public/yaml/comment/delete.yaml"
        ret = self.get_data_config.get_data_post(file_path)

        # 组装请求数据
        url = ret['url']
        header = ret['header']
        post_data = ret['expect']['retData']
        ret_result = []

        # 循环用例，请求获取数据
        for data in post_data:
            # 请求api获取结果
            params = self.comment_post.send_post(url, data, header)

            # 判断status
            result_status = self.validator.validate_status(ret['expect'], params)
            if result_status == 'fail':
                result = 500
            data['result_data'] = result_status
            data['result_value'] = ''
            ret_result.append(data)

            # 写入html
            msg = params['message']
            self.get_html_data.set_html(url, result_status, data, '评论', msg)

        # 写入结果yaml
        file_request_path = "/public/yaml/comment/delete_request.yaml"
        self.comment_list_data.set_to_yaml(file_request_path, ret_result)

        return result

    # 删除回复
    def delete_replay(self):
        result = 200
        # 获取文件请求数据
        file_path = "/public/yaml/comment/delete_replay.yaml"
        ret = self.get_data_config.get_data_post(file_path)

        # 组装请求数据
        url = ret['url']
        header = ret['header']
        post_data = ret['expect']['retData']
        ret_result = []

        # 循环用例，请求获取数据
        for data in post_data:
            # 请求api获取结果
            params = self.comment_post.send_post(url, data, header)

            # 判断status
            result_status = self.validator.validate_status(ret['expect'], params)
            if result_status == 'fail':
                result = 500

            data['result_data'] = result_status
            data['result_value'] = ''
            ret_result.append(data)
            # 写入html
            msg = params['message']
            self.get_html_data.set_html(url, result_status, data, '评论', msg)
        # 写入结果yaml
        file_request_path = "/public/yaml/comment/delete_replay_request.yaml"
        self.comment_list_data.set_to_yaml(file_request_path, ret_result)

        return result

    # 获取详情
    def get_detail(self):
        result = 200
        # 获取文件请求数据
        file_path = "/public/yaml/comment/get_detail.yaml"
        ret = self.get_data_config.get_data_post(file_path)

        # 组装请求数据
        url = ret['url']
        header = ret['header']
        post_data = ret['expect']['retData']
        ret_result = []

        for data in post_data:
            params = self.comment_post.send_post(url, data, header)
            result_status = self.validator.validate_status(ret['expect'], params)
            if result_status == 'fail':
                result = 500

            data['result_data'] = result_status
            data['result_value'] = ''
            ret_result.append(data)

            # 写入html
            msg = params['message']
            self.get_html_data.set_html(url, result_status, data, '评论', msg)
        # 写入结果yaml
        file_request_path = "/public/yaml/comment/get_detail_request.yaml"
        self.comment_list_data.set_to_yaml(file_request_path, ret_result)
        return result

    # 获取标签列表
    def get_label_list(self):
        result = 200
        # 获取文件请求数据
        file_path = "/public/yaml/comment/get_detail.yaml"
        ret = self.get_data_config.get_data_post(file_path)

        # 组装请求数据
        url = ret['url']
        header = ret['header']
        post_data = ret['expect']['retData']
        ret_result = []

        for data in post_data:
            params = self.comment_post.send_post(url, data, header)

            result_status = self.validator.validate_status(ret['expect'], params)
            if result_status == 'fail':
                result = 500
            data['result_data'] = result_status
            data['result_value'] = ''
            ret_result.append(data)

            # 写入html
            msg = params['message']
            self.get_html_data.set_html(url, result_status, data, '评论', msg)

        # 写入结果yaml
        file_request_path = "/public/yaml/comment/get_label_list_request.yaml"
        self.comment_list_data.set_to_yaml(file_request_path, ret_result)

        return result


if __name__ == '__main__':
    run = CommentData()
    run.list()
