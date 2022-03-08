# !/usr/bin python3                                 
# encoding: utf-8 -*-                            
# @author: 沙陌 微信：Matongxue_2
# @Time: 2021/10/20 21:04
# @Copyright：北京码同学
from pages.login_page import LoginPage


class LoginActions:

    def login(self,username='18729399607',password='abc123456'):
        login_page = LoginPage()
        login_page.click_pwd_login()
        login_page.send_keys_username(username)
        login_page.send_keys_password(password)
        return login_page.click_login_btn()