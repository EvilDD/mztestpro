import unittest
from models import myunit, function
from time import sleep
from page_obj.omsGoodsUploadPage import addProucts
from page_obj.loginPage import omslogin


class productAdd(myunit.MyTest):
    '''oms商品批量上传用例'''

    def loginDo(self):
        self.db = function.postgreSql()
        customerCode = self.db.consOderBy()
        self.oms_login_verify(username=customerCode)
        omslogin(self.driver).warehouse_login('GZBY')  # 选择仓库完全登录
        self.po = addProucts(self.driver)

    def test1(self):
        '''商品模板'''
        # self.loginDo()
        # self.po.download()
        # function.insert_img(self.driver, '2222222222.jpg')
        # sleep(10)
        a = function.excel('product_import.xls')
        posVal = a.getDataPosVal()
        posVal['商品SKU1'][1] = '睡觉'
        a.creatExcel(posVal)

if __name__ == '__main__':
    unittest.main()
