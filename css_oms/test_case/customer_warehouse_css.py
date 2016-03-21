import unittest
from models import myunit, function
from time import sleep
from page_obj.cusHousePage import addWarehouse
from page_obj.loginPage import omslogin


class cusWareHouseTest(myunit.MyTest):
    '''新客户分配交货仓,默认GZBY仓,海关->电子口岸,商检->电子口岸,代备案都为是'''
    text = {
        'a': '广州白云',
        'b': '广州机场快件处理中心',
        'c': '香港上水',
        'd': '联邦',
        'e': '广州海关－电子口岸',
        'f': '广州海关－上海元亨',
        'g': '广州商检－电子口岸',
        'h': '广州商检－智检平台',
        'i': '平台代用户发送海关与国检报文',
        'j': '用户自行发送海关与国检报文',
        'k': '平台仅代用户发送海关报文',
        'l': '平台仅代用户发送国检报文',
    }
    newHouse = [
        'C0001',
        text['a'],
        text['e'],
        text['g'],
        'hgtdspt',
        'hgqyzch',
        'hgptbah',
        'hgqybah',
        'sjptbah',
        'sjqybah',
        text['i'],
        text['i']
    ]

    def loginDo(self):
        self.db = function.postgreSql()
        self.css_login_verify()
        self.po = addWarehouse(self.driver)

    def test_wareHouse1(self):
        '''新客户分配默认配置,上面大用例模块介绍,未强调为默认值'''
        self.loginDo()
        self.newHouse[0] = self.db.consOderBy()  # 客户代码更改为最新客户
        self.po.addCusWarehouse(self.newHouse)  # 新客户添加GZBY仓库
        self.oms_login_verify(username=self.newHouse[0])  # 新客户登陆oms
        self.assertEqual(omslogin(self.driver).oms_login_suc(), self.newHouse[0])
        self.assertEqual(omslogin(self.driver).warehouse_login_suc(), 'GZBY')
        function.insert_img(self.driver, 'gzby_11111.jpg')  # 1代表仓库、电子口岸、代备案

    def test_wareHouse2(self):
        '''新客户分配GZBYBC仓,海关->元享,商检->智检'''
        self.loginDo()
        self.newHouse[0] = self.db.consOderBy()  # 客户代码更改为最新客户
        self.newHouse[1] = self.text['b']  # GZBYBC仓库
        self.newHouse[2] = self.text['f']  # 元享
        self.newHouse[3] = self.text['h']  # 智检
        self.po.addCusWarehouse(self.newHouse)  # 新客户添加仓库信息
        self.oms_login_verify(username=self.newHouse[0])  # 新客户登陆oms
        omslogin(self.driver).warehouse_login('GZBYBC')  # 选择仓库
        self.assertEqual(omslogin(self.driver).oms_login_suc(), self.newHouse[0])
        self.assertEqual(omslogin(self.driver).warehouse_login_suc(), 'GZBYBC')
        function.insert_img(self.driver, 'gzbybc_22111.jpg')

    def test_wareHouse3(self):
        '''HKSS仓,海关->电子口岸,商检->智检'''
        self.loginDo()
        self.newHouse[0] = self.db.consOderBy()  # 客户代码更改为最新客户
        self.newHouse[1] = self.text['c']  # HKSS仓库
        self.newHouse[2] = self.text['e']  # 口岸
        self.newHouse[3] = self.text['h']  # 智检
        self.po.addCusWarehouse(self.newHouse)  # 新客户添加仓库信息
        self.oms_login_verify(username=self.newHouse[0])  # 新客户登陆oms
        omslogin(self.driver).warehouse_login('HKSS')  # 选择仓库
        self.assertEqual(omslogin(self.driver).oms_login_suc(), self.newHouse[0])
        self.assertEqual(omslogin(self.driver).warehouse_login_suc(), 'HKSS')
        function.insert_img(self.driver, 'gzbybc_21111.jpg')


if __name__ == '__main__':
    unittest.main()
