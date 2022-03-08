# !/usr/bin python3                                 
# encoding: utf-8 -*-                            
# @author: 沙陌 微信：Matongxue_2
# @Time: 2021/10/20 20:59
# @Copyright：北京码同学
from pages.base_page import BasePage


class HomePage(BasePage):

    def click_mine_menu(self):
        # ele_info = {'name':'登录链接','type':'linktext','value':'登录','timeout':5}
        ele_info = self.page_eles['我的菜单']
        self.driver.click(ele_info)
    def click_home_menu(self):
        # ele_info = {'name':'登录链接','type':'linktext','value':'登录','timeout':5}
        ele_info = self.page_eles['首页菜单']
        self.driver.click(ele_info)