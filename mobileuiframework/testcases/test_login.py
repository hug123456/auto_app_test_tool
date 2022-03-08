# !/usr/bin python3                                 
# encoding: utf-8 -*-                            
# @author: 沙陌 微信：Matongxue_2
# @Time: 2021/10/20 21:07
# @Copyright：北京码同学
import pytest

from actions.login_actions import LoginActions


class TestLogin:

    def test_login(self):
        home_page = LoginActions().login()
        home_page.click_mine_menu()
        flag = home_page.driver.page_contains('沙陌1')
        pytest.assume(flag == True)