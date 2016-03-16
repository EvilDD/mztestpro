import unittest
from models import myunit, function
from page_obj.loginPage import csslogin


class cssloginTest(myunit.MyTest):
    '''css后台登录测试'''

    def test_csslogin1(self):
        '''用户名不存在'''
        username = 'abcdefggfedcba'
        self.css_login_verify(username=username)
        po = csslogin(self.driver)
        self.assertEqual(po.user_error_hint(), '该用户不存在！')
        function.insert_img(self.driver, 'noUser.jpg')

    def test_csslogin2(self):
        '''用户名存在, 密码错误'''
        password = '000000'
        self.css_login_verify(password=password)
        po = csslogin(self.driver)
        self.assertEqual(po.pw_error_hint(), '密码错误！')
        function.insert_img(self.driver, 'password_err.jpg')

    def test_csslogin3(self):
        '''用户名密码正确，验证码错误'''
        captcha = 'aaaaa'  # 不符合前台输入要求时，不弹窗
        self.css_login_verify(captcha=captcha)
        po = csslogin(self.driver)
        self.assertEqual(po.captcha_error_hint(), '验证码输入不正确！')
        function.insert_img(self.driver, 'captcha_err.jpg')

    def test_csslogin4(self):
        '''admin登陆GZBY成功用例'''
        username = 'admin'
        password = '123123'
        self.css_login_verify(username=username, password=password)
        po = csslogin(self.driver)
        self.assertEqual(po.user_login_suc(), username)
        self.assertEqual(po.warehouse_login_suc(), 'GZBY')
        function.insert_img(self.driver, 'gzby_in.jpg')

    def test_csslogin5(self):
        '''admin登陆GZBYBC成功'''
        username = 'admin'
        password = '123123'
        warehouse = '广州机场快件处理中心---GZBYBC'
        self.css_login_verify(username=username, password=password, warehouse=warehouse)
        po = csslogin(self.driver)
        self.assertEqual(po.user_login_suc(), username)
        self.assertEqual(po.warehouse_login_suc(), 'GZBYBC')
        function.insert_img(self.driver, 'gzbybc_in.jpg')

    def test_csslogin6(self):
        '''admin登陆HKSS成功'''
        username = 'admin'
        password = '123123'
        warehouse = '香港上水---HKSS'
        self.css_login_verify(username=username, password=password, warehouse=warehouse)
        po = csslogin(self.driver)
        self.assertEqual(po.user_login_suc(), username)
        self.assertEqual(po.warehouse_login_suc(), 'HKSS')
        function.insert_img(self.driver, 'hkss_in.jpg')

    def test_csslogin7(self):
        '''admin登陆GZFEDEXBC成功'''
        username = 'admin'
        password = '123123'
        warehouse = '联邦---GZFEDEXBC'
        self.css_login_verify(username=username, password=password, warehouse=warehouse)
        po = csslogin(self.driver)
        self.assertEqual(po.user_login_suc(), username)
        self.assertEqual(po.warehouse_login_suc(), 'GZFEDEXBC')
        function.insert_img(self.driver, 'gzfedexbc_in.jpg')

if __name__ == '__main__':
    unittest.main()
