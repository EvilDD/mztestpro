from selenium import webdriver
import os
import psycopg2
import re
from xlrd import open_workbook
from xlwt import Workbook
from collections import OrderedDict


def insert_img(driver, file_name):
    '''截图函数'''
    base_dir = os.path.dirname(os.path.dirname(__file__))  # test_case目录下
    base_dir = base_dir.replace('\\', '/')
    base = base_dir.split('/test_case')[0]  # test_case上级目录
    file_path = base + '/report/image/' + file_name
    # print(file_path)
    driver.get_screenshot_as_file(file_path)  # 截屏


class excel(object):
    '''操作excel表格'''

    def __init__(self, fileName):
        super(excel, self).__init__()
        casePath = os.path.dirname(os.path.dirname(__file__))  # test_case目录下
        dataPath = os.path.dirname(casePath)
        self.file = dataPath + '\\data\\' + fileName

    def getDataPosition(self):
        '''获取表格列表名称,保存第一列数据位置,字典形式,商品sku:(1,0)代表sku值的位置'''
        try:
            data = open_workbook(self.file)  # formatting_info=True保留数据格式
        except Exception as e:
            print(e, '获取%s文件失败' % self.file)
        table = data.sheets()[0]  # 通过索引获取第一张sheet表
        excelDict = OrderedDict()  # 创建一个有序的字典存放数据在第几行和对应值
        for row in range(table.nrows):  # 有几行数据就循环几次
            rowsData = table.row_values(row)  # 读取所有的整行数据
            for col in range(table.ncols):
                print(rowsData[col] + repr(row))
                excelDict[rowsData[col] + repr(row)] = [col, table.cell(row, col).value]  # 多行数据
        for a, b in excelDict.items():
            print(a, b)
        return excelDict

    def creatExcel(self):
        wb = Workbook()
        ws = wb.add_sheet('Sheet1')
        col = self.getDataPosition()
        print(col['商品SKU'])
        # ws.write(1, 0, 'proskutest')
        for a, b in col.items():
            print(a, b)
        wb.save(self.file)


class postgreSql(object):
    """操作数据库"""

    def __init__(self):
        super(postgreSql, self).__init__()
        self.conn = psycopg2.connect(database='testnewoms', user='postgres', password='123123', host='192.168.0.252', port='5432')
        self.cur = self.conn.cursor()

    def isConsExist(self, customerCode):
        # 判断给的客户代码是否存在，存在返回True
        order = "select * from tbl_customer where customer_code='%s'" % customerCode
        self.cur.execute(order)
        rows = self.cur.fetchall()
        if rows == []:
            return False
        else:
            return True

    def tableCount(self, table):
        # 返回表中有多少条记录
        order = "select  count (*) from %s" % table
        self.cur.execute(order)
        count = self.cur.fetchone()
        return count[0]

    def consOderBy(self, col='customer_code', table='tbl_customer'):
        # 默认找出最后新增的客户代码
        # 找出某张表某列倒序第一个数据
        order = "SELECT %s FROM %s ORDER BY %s DESC" % (col, table, col)
        self.cur.execute(order)
        code = self.cur.fetchone()
        return code[0]

    def proStringNo(self, col, table):
        # 创建数据库不存在的字符串，如sku，支付单号等
        # 倒序某列数据然后有数值的+1,没有加字符1
        sku = self.consOderBy(col, table)  # 最新数据
        num = re.search('\d*$', sku).group(0)  # 分离出字符串结尾的数字
        if num == '':  # 判断分享出的字符结尾如果没有数字就加个0
            num = '0'
        else:
            numLen1 = len(num)
            num_add = repr(int(num) + 1)  # 给字符串末尾的数值加1生成新字符 串
            numLen2 = len(num_add)
            if numLen1 != numLen2:  # 如X10排在X9后,X100,排除数值加1后生成多位数
                num += '0'
            else:
                num = num_add
        newNum = re.sub('\d*$', num, sku)
        return newNum

    def __del__(self):
        self.conn.close()
        del self.conn


if __name__ == "__main__":
    a = postgreSql()
    print(a.proStringNo('product_sku', 'tbl_product'))

a = {
    '海关商品备案号': '1232556',
    '品牌': '品牌',
    '商品单位': '瓶',
    '商品链接': 'http://www.google.com',
    '条码类型': '默认条码',
    '规格型号': '15*12',
    '行邮税号': '01000000',
    'CIQ商检备案号': 562159.0,
    '商品净重': 1.2,
    '备注': 'beizhu1',
    '有无保质期': '有',
    '商品条码': 'C250-123456789',
    '原产国': '阿根廷',
    '包装规格': '',
    '商品分类': '保健护理用品',
    '商品货号': '',
    '申报价格': 12.1,
    '商品SKU': '123456780',
    '国际编码': '',
    '包装种类': '4M(纸箱)',
    '商品名称': '111',
    '是否礼品': '否',
    '申报币种': 'RMB',
    '商品毛重': 1.2,
    '商品英文名称': 'abc',
    '体积（平方米）': '',
    '海关编码': '0106311000',
    '海关品名': '品名',
    '生产厂家': '厂家'
}
