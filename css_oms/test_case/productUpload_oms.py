import unittest
from models import myunit, function
from time import sleep
from page_obj.omsGoodsUploadPage import addProucts
from page_obj.loginPage import omslogin


class productAdd(myunit.MyTest):
    '''oms商品管理->商品批量上传'''
    '''Chrome排除,浏览器上传content-type问题'''

    def loginDo(self):
        self.db = function.postgreSql()
        customerCode = self.db.consOderBy()
        self.oms_login_verify(username=customerCode)
        omslogin(self.driver).warehouse_login('GZBY')  # 选择仓库完全登录
        self.po = addProucts(self.driver)

    def test1(self):
        '''单条商品上传'''
        self.loginDo()
        excel = function.excel('product_import.xls')
        posVal = excel.getDataPosVal()
        posVal['商品SKU1'][1] = self.db.proStringNo('product_sku', 'tbl_product')
        excel.creatExcel(posVal)
        self.po.uploadLogin('product_import.xls')
        self.assertEqual(self.po.mesUpload(), '上传成功！')
        function.insert_img(self.driver, 'proUpSuc.jpg')

    def test2(self):
        '''已存在商品sku上传'''
        self.loginDo()
        self.po.uploadLogin('product_import.xls')
        assert('商品SKU' and '已存在' in self.po.mesUpload())
        function.insert_img(self.driver, 'proUpExist.jpg')

    def test3(self):
        '''多个商品上传'''
        self.loginDo()
        excel = function.excel('product_import1.xls')
        posVal = excel.getDataPosVal()
        posVal['商品SKU1'][1] = self.db.proStringNo('product_sku', 'tbl_product')
        posVal['商品SKU2'][1] = function.stringAddOne(posVal['商品SKU1'][1])
        excel.creatExcel(posVal)
        self.po.uploadLogin('product_import1.xls')
        self.assertEqual(self.po.mesUpload(), '上传成功！')
        function.insert_img(self.driver, 'moreProUpSuc.jpg')

    def test4(self):
        '''多商品上传相同sku'''
        self.loginDo()
        self.po.uploadLogin('product_import1.xls')
        assert('商品SKU' and '已存在' in self.po.mesUpload())
        function.insert_img(self.driver, 'moreproUpExist.jpg')

# 商品批量上传,表格sku按照顺序读取上传,遇到重复停止上传,在未到重复的sku全部上传成功
if __name__ == '__main__':
    unittest.main()
