# !/usr/bin python3                                 
# encoding: utf-8 -*-                            
# @author: 沙陌 微信：Matongxue_2
# @Time: 2021/10/20 21:01
# @Copyright：北京码同学
from pages.base_page import BasePage
from pages.home_page import HomePage


class LoginPage(BasePage):

    def click_pwd_login(self):
        # ele_info = {'name':'登录链接','type':'linktext','value':'登录','timeout':5}
        ele_info = self.page_eles['帐号密码登录']
        self.driver.click(ele_info)
    def send_keys_username(self,username):
        # ele_info = {'name':'登录链接','type':'linktext','value':'登录','timeout':5}
        ele_info = self.page_eles['用户名输入框']
        self.driver.send_keys(ele_info,username)
    def send_keys_password(self,password):
        # ele_info = {'name':'登录链接','type':'linktext','value':'登录','timeout':5}
        ele_info = self.page_eles['密码输入框']
        self.driver.send_keys(ele_info,password)
    def click_login_btn(self):
        # ele_info = {'name':'登录链接','type':'linktext','value':'登录','timeout':5}
        ele_info = self.page_eles['登录按钮']
        self.driver.click(ele_info)
        return HomePage()