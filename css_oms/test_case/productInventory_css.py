import unittest
from models import myunit, function
from page_obj.cssProInventorypage import inventPage
from time import sleep


class proInventory(myunit.MyTest):
    '''css商品管理->库存管理'''

    def loginDo(self):
        self.db = function.postgreSql()
        self.customerCode = self.db.consOderBy()
        self.proSku = self.db.consOderBy('product_sku', 'tbl_product')
        self.db.proRecord(self.proSku)  # 商品备案
        self.css_login_verify()
        self.po = inventPage(self.driver)

    def test1(self):
        '''单个商品库存上传'''
        # 上传一个最新客户的最新商品10个库存
        self.loginDo()
        excel = function.excel('product_inventory_import.xlsx')
        posVal = excel.getDataPosVal()
        posVal['客户代码1'][1] = self.customerCode
        posVal['商品SKU1'][1] = self.proSku
        num = self.db.InventoryNum()
        excel.creatExcel(posVal)
        self.po.inventoryUpload('product_inventory_import.xlsx')
        num1 = self.db.InventoryNum()
        self.assertEqual(num + 10, num1)
        function.insert_img(self.driver, 'addProInventory.jpg')

if __name__ == '__main__':
    unittest.main()
