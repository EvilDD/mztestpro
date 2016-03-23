import unittest
from models import myunit, function
from time import sleep
from page_obj.customerInfoPage import cusInfo
from page_obj.loginPage import omslogin


class cusInfoTest(myunit.MyTest):
    '''admin-GZBY创建新客户'''

    newCus = [
        'Evil',
        '000000',
        '18626241903',
        '0755-6210890',
        '1992349278@qq.com',
        '海购通',
        'HGT',
        'YXD',
        'http://www.ihaixie.com'
    ]

    def loginDo(self):
        self.db = function.postgreSql()
        self.css_login_verify()
        self.po = cusInfo(self.driver)

    def test_customer0(self):
        '''新增时客户代码不为空, 且数据库中不存在该客户代码'''
        self.loginDo()
        self.po.iframe_page()  # 客户资料iframe界面
        self.po.newPage()  # 点击新增
        customerCode = self.po.cusCode()
        if customerCode == '' or self.db.isConsExist(customerCode):
            function.insert_img(self.driver, 'add_customer_exist.jpg')
            raise AssertionError("该客户代码已存在或者客户代码为空")  # assert显示失败为F,其他异常为E
        else:
            print(customerCode)

    def test_customer1(self):
        '''成功添加新客户'''
        self.loginDo()
        num1 = self.db.tableCount('tbl_customer')
        self.po.add_customer(self.newCus)
        sleep(0.3)
        num2 = self.db.tableCount('tbl_customer')
        self.assertEqual(num1 + 1, num2)
        function.insert_img(self.driver, 'add_customer_suc.jpg')

    def test_customer2(self):
        '''禁用客户'''
        self.loginDo()
        self.po.forbiCustomer()  # 禁用客户
        username = self.po.offCusCode()
        self.oms_login_verify(username=username)
        self.assertEqual(omslogin(self.driver).error_message(), '该用户已被禁用！')
        function.insert_img(self.driver, 'forbiCustomer.jpg')

    def test_customer3(self):
        '''启用客户'''
        self.loginDo()
        self.po.usingCustomer()  # 启用客户
        username = self.po.offCusCode()  # 返回刚禁用客户代码
        self.oms_login_verify(username=username)
        if omslogin(self.driver).error_message() == '该用户已被禁用！':
            raise AssertionError('启用按钮无效')
            function.insert_img('startCustomer_err.jpg')
        else:
            print(omslogin(self.driver).error_message())

if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(add_consumer("test_newConsumer"))
    # suite.addTest(add_consumer("test_a"))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)
