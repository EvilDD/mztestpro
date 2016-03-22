import unittest
from models import myunit, function
from time import sleep
from page_obj.omsGoodsAddPage import addProuct
from page_obj.loginPage import omslogin
import re


class productAdd(myunit.MyTest):
    '''oms商品新增用例,此次商品均为代备案模式'''
    proList = {
        'product_sku': 'AAAAAA0',
        'product_name': 'proName',
        'product_en_name': 'EnglishName',
        'supplier_code': 'GYSCode',
        'product_spu': 'SPHH',
        'pack_spec': 'BZGG',
        'price': '1',
        'net_weight': '1',
        'gross_weight': '2',
        'note': 'Just test',
        'product_images': 'http://img',
        'brand': 'PingPai',
        'manufactory': 'SCCJ',
        'hs_product_name': 'HGPP',
        'product_spec': 'GGXJ',
        'serial_no': 'serialNo',
        'cube': '1',
        'product_link': 'http://www.ihaixie.com'
    }

    def loginDo(self):
        self.db = function.postgreSql()
        customerCode = self.db.consOderBy()
        self.oms_login_verify(username=customerCode)
        self.po = addProuct(self.driver)

    def proSkuNo(self):
        # 倒序sku然后有数值的+1,没有加字符1
        sku = self.db.consOderBy('product_sku', 'tbl_product')  # 最新产品sku
        num = re.search('\d*$', sku).group(0)  # 分离出商品sku结尾的数字
        if num == '':  # 判断商品sku结尾如果没有数字就加个0
            num = '0'
        else:
            numLen1 = len(num)
            num_add = repr(int(num) + 1)  # 给商品sku末尾的数值加1生成新sku
            numLen2 = len(num_add)
            if numLen1 != numLen2:  # 如X10排在X9后,X100,排除数值加1后生成多位数
                num += '0'
            else:
                num = num_add
        newNum = re.sub('\d*$', num, sku)
        return newNum

    def test1(self):
        '''添加新商品,数据库倒序产品sku再+1'''
        self.loginDo()
        omslogin(self.driver).warehouse_login('GZBY')  # 选择仓库完全登录
        proNums1 = self.db.tableCount('tbl_product')  # 添加前商品条数
        self.proList['product_sku'] = self.proSkuNo()  # 返回一个数据库不存在的sku
        self.po.add_pro(self.proList)  # 添加商品
        sleep(0.3)
        proNums2 = self.db.tableCount('tbl_product')  # 添加后商品条数
        self.assertEqual(proNums1 + 1, proNums2)
        function.insert_img(self.driver, 'oms_add_product.jpg')
        sleep(30)

    # def test2(self):
        '''添加当前仓库已存在的商品sku'''


if __name__ == '__main__':
    unittest.main()
