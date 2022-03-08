# !/usr/bin python3                                 
# encoding: utf-8 -*-                            
# @author: 沙陌 微信：Matongxue_2
# @Time: 2021/9/13 21:11
# @Copyright：北京码同学
from common.driver import GlobalDriver
from common.file_load import load_yaml_file


class BasePage:

    # 一个构造方法，将自己封装的driver对象传递过来
    def __init__(self):
        self.driver = GlobalDriver.driver
        self.douban_eles = load_yaml_file('/pagefiles/douban.yml')
        # 得到当前类名称
        self.class_name = self.__class__.__name__
        self.page_eles = self.douban_eles[self.class_name]