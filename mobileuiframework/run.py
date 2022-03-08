# !/usr/bin python3                                 
# encoding: utf-8 -*-                            
# @author: 沙陌 微信：Matongxue_2
# @Time: 2021/6/20 13:51
# @Copyright：北京码同学网络科技有限公司
import os

import pytest

if __name__ == '__main__':
    # 执行时会按照pytest.ini这个配置所配的相关信息进行执行
    pytest.main()
    os.system('allure generate ./report/shop -o ./report/html --clean')
