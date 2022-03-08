# !/usr/bin python3                                 
# encoding: utf-8 -*-                            
# @author: 沙陌 微信：Matongxue_2
# @Time: 2021/9/27 20:49
# @Copyright：北京码同学



# 解析action文件并执行操作
import os
import re

import allure
import pytest

from common.driver import GlobalDriver
from common.file_load import load_yaml_file


# 定义一个字典，专门用来存储每一个业务对应的默认参数
from setting import DIR_NAME

actions_variables = {} #这里用来存储所有业务里的默认变量，
# {“买家登录业务”:{"username":"shamo","password":"123456"},"创建订单业务":{"keyword":"炒锅"},"添加地址":{"name":"xxx"}}


# 定义一个字典，专门用来存储每一个测试用例用到的参数数据
testcase_varibales = {} #{“买家登录业务”:{"username":"shamo","password":"123456"}}

def regx_sub(string,action_name):
    """
    正则匹配某个字符串中的所有变量${xxxxx}调用，并从vars_dict中取出该变量对应值进行替换
    :param string:
    :return:
    """
    res_all = re.findall(r'\$\{([^\{].+?)\}', str(string)) #从目标字符串中匹配出所有的变量名称
    # 变量匹配到的所有变量名称
    for var_name in res_all:


        # 优先选择testcase_varibales里的业务对应的变量进行替换#{“买家登录业务”:{"username":"shamo1","password":"123456"}}
        # 如果用例变量里没有，则从actions_variables得到对应的业务存储的默认变量字典 #{“登录业务”:{"username":"shamo","password":"123456"}}
        if action_name in testcase_varibales:
            print('匹配testcase_varibales')
            if var_name in testcase_varibales[action_name]:
                var_value = testcase_varibales[action_name][var_name]

            elif var_name in actions_variables[action_name]:
                var_value = actions_variables[action_name][var_name]
            else:
                raise Exception('变量{}不存在'.format(var_name))
        elif action_name in actions_variables:
            print('匹配actions_variables:{}'.format(actions_variables))
            if var_name in actions_variables[action_name]:
                var_value = actions_variables[action_name][var_name]
            else:
                raise Exception('变量{}不存在'.format(var_name))
        else:
            raise Exception('变量{}不存在'.format(var_name))
        print('value:{}'.format(var_value))

        # 使用正则替换目标字符串中的变量
        string = re.sub(r'\$\{'+var_name+r'\}', str(var_value), string)
    return string


def exec_action(yml):
    yaml_context = load_yaml_file(yml) #读取某个action文件，得到里边所有的内容
    action_name = yaml_context['name'] #得到业务名称
    pagefile = yaml_context['pagefile'] #得到对应的pagefile路径
    page_els = load_yaml_file(pagefile)
    # 业务的默认变量不一定有
    if 'variables' in yaml_context:
        variables = yaml_context['variables'] #得到当前业务对应的默认变量
        # 将得到的当前业务默认变量存入全局的业务变量默认对象中
        actions_variables[action_name] = variables
    steps = yaml_context['steps'] #得到业务对应的所有步骤，steps是一个列表
    # 拿到步骤以后遍历所有步骤
    for step in steps:
        # step表示的每一步，他是一个字典
        if 'page' in step:
            page_name = step['page']
        if 'element' in step:
            element_name = step['element']
        operate = step['operate']
        if 'param' in step:
            param = step['param']
            # 拿到的很可能是一个变量${username},那么我们需要进行变量替换
            param = regx_sub(param,action_name)
        #通过page_name及element_name拿到元素的定位信息
        ele_info = page_els[page_name][element_name]

        # 根据操作名称去调用driver里相关的操作
        # if operate == 'click':
        #     GlobalDriver.driver.click(ele_info)
        # elif operate == 'send_keys':
        #     GlobalDriver.driver.send_keys(ele_info,param)

        # 以上判断会有很多，那么在python可以采用反射的机制来完成
        if hasattr(GlobalDriver.driver, operate):
            func = getattr(GlobalDriver.driver, operate)  # 得到函数对象
            params_count = func.__code__.co_argcount - 1  # 因为实例方法有一个默认的self，所以减掉1
            default = func.__defaults__  # 获取对象方法参数里的默认值,(5,)是个元组
            # 判断方法定义里的参数个数，来决定反射执行方法时如何传参
            if params_count > 1:
                if param == None:  # 如果param不为none，说明没有参数，那么元素和默认参数值一起传
                    func_param = [ele_info, *default]
                else:
                    func_param = [ele_info, param]
                func(*func_param)
            elif params_count == 0:  # 如果我的方法定义里没有参数
                func()
            else:  # 如果方法定义只有一个参数，要么你传的是元素，要么你传的param
                if 'element' in step:
                    func(ele_info)
                elif 'param' in step:
                    func(param)
                else:
                    func(*default)
        else:
            raise Exception('在【{}】里【{}】操作【{}】不正确'.format(pagefile, page_name, operate))

    #
    # print(yaml_context)
    # print(type(yaml_context))
"""
1. 遍历testcases目录下所有的yml文件，得到里边所有的测试用例，形成下面的数据结构
    [
        ['登录用户名错误',{'name':'登录用户名错误','action':'/keyword/actions/buyer_login_action.yml','params':{'username':'shamo1'},'validate':[{'type':'page_contains','expect':'账号密码错误']}],
        ['登录密码错误',{'name':'登录密码错误','action':'/keyword/actions/buyer_login_action.yml','params':{'password':'2335455'},'validate':[{'type':'page_contains','expect':'账号密码错误']}],
        ['登录用户名不存在',{'name':'登录用户名不存在','action':'/keyword/actions/buyer_login_action.yml','params':{'username':'rtfgfgg'},'validate':[{'type':'page_contains','expect':'账号密码错误']}],
        ['创建订单成功',{'name':'创建订单成功','preactions':[{'action':'/keyword/actions/buyer_login_action.yml'}],'action':'/keyword/actions/create_order_action.yml','validate':[{'type':'page_contains','expect':'账号密码错误']}],
    ]
2. 第一步解析得到的数据结构，非常适合pytest的参数化形式
3. 在pytest测试方法上使用pytest参数化形式
"""

# 实现第一步
def get_all_testcases():
    # 获取指定目录下的所有文件名称
    testcase_file_list = os.listdir(DIR_NAME + '/keyword/testcases')
    testcase_all_list = []  # 用例存储所有的测试用例关键字数据
    # 遍历所有的文件名称列表testcase_file_list
    for testcase_file_name in testcase_file_list:
        # 拼接出测试用例集合文件路径
        testcase_file_path = f'/keyword/testcases/{testcase_file_name}'
        testcases_list = load_yaml_file(testcase_file_path)['testcases']
        for testcase in testcases_list:
            testcase_name = testcase['name']
            # 将测试用例名称和测试用例所有的信息组合成一个列表，并且追加到testcase_all_list中
            testcase_data = [testcase_name,testcase]
            testcase_all_list.append(testcase_data)
    return testcase_all_list
"""
{   'name':'登录用户名错误',
    'action':'/keyword/actions/buyer_login_action.yml',
    'params':{'username':'shamo1'},
    'validate':[
        {'type':'page_contains',
        'expect':'账号密码错误'}
        ]
"""
# {'name':'登录用户名错误','action':'/keyword/actions/buyer_login_action.yml','params':{'username':'shamo1'},'validate':[{'type':'page_contains','expect':'账号密码错误']}
def exec_testcase(testcase):
    if 'preactions' in testcase:
        preactions = testcase['preactions'] #得到是前置业务列表 [{'action':'/keyword/actions/buyer_login_action.yml'}]
        for actions in preactions:
            action_file_path = actions['action'] #得到前置业务对应的业务文件路径
            preaction_action_name = load_yaml_file(action_file_path)['name'] #获取前置业务名称
            if preaction_action_name in testcase_varibales:
                del testcase_varibales[preaction_action_name]  # 清除当前业务在测试用例变量字典中的数据
            exec_action(action_file_path) #执行前置业务对应的操作
    action_path = testcase['action'] #得到该用例对应的业务文件路径
    action_name = load_yaml_file(action_path)['name'] #获取业务对应的名称
    if action_name in testcase_varibales:
        del testcase_varibales[action_name]  # 清除当前业务在测试用例变量字典中的数据
    if 'params' in testcase:
        params = testcase['params'] # {'username':'shamo1'}, 这是个字典
        testcase_varibales[action_name] = params #将测试用例数据按照对应的业务名称存储在全局的测试用例数据变量中
    # 所有的数据都准备好以后，执行测试用例
    exec_action(action_path)
    # 执行完成之后要处理断言
    validate_list = testcase['validate'] #得到断言列表
    for validate in validate_list:
        #得到断言类型
        type = validate['type']
        # 得到断言的期望值
        expect = validate['expect']
        if type == 'page_contains':
            pytest.assume(GlobalDriver.driver.page_contains(expect) == True)

@pytest.mark.parametrize('testcase_name,testcase',get_all_testcases())
@allure.title('{testcase_name}')
def test_keyword(testcase_name,testcase):
    # exec_action('/keyword/actions/buyer_login_action.yml')
    exec_testcase(testcase)
if __name__ == '__main__':
    print(get_all_testcases())

