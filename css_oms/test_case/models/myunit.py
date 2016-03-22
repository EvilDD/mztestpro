# from selenium import webdriver
from .driver import browser
import unittest
from page_obj.loginPage import csslogin, omslogin
# import os


class MyTest(unittest.TestCase):
    '''继承uittest类,test_case调用不用重复写setUp和tearDown方法'''

    def setUp(self):
        self.driver = browser()
        self.driver.implicitly_wait(10)
        # self.driver.set_window_size(1000, 900)
        self.driver.maximize_window()  # phantomjs不设置全屏,默认小屏读取不到页面元素

    def css_login_verify(self, username='admin', password='123123', warehouse='广州白云---GZBY', captcha='zyd'):
        '''css公共登录模块'''
        csslogin(self.driver).admin_login(username, password, warehouse, captcha)

    def oms_login_verify(self, username='C0001', password='000000', captcha='zyd'):
        '''oms公共登录模块'''
        omslogin(self.driver).customer_login(username, password, captcha)

    def tearDown(self):
        self.driver.quit()
