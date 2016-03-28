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


def stringAddOne(string):
    '''输入一个字符串,返回一个新的+1字符串'''
    num = re.search('\d*$', string).group(0)  # 分离出字符串结尾的数字
    if num == '':  # 判断分享出的字符结尾如果没有数字就加个0
        num = '0'
    else:
        zeroNum = ''
        temNum = 0
        for char in num:  # 000010
            if char == '0':
                temNum += 1
            else:
                break
        for i in range(temNum):  # 返回数字前面的0000
            zeroNum += '0'
        numLen1 = len(repr(int(num)))
        num_add = repr(int(num) + 1)  # 给字符串末尾的数值加1生成新字符 串
        numLen2 = len(num_add)
        if numLen1 != numLen2:  # 如X10排在X9后,X100,排除数值加1后生成多位数
            num += '0'
        else:
            num = zeroNum + num_add
    newString = re.sub('\d*$', num, string)
    return newString


class excel(object):
    '''操作excel表格'''

    def __init__(self, fileName):
        super(excel, self).__init__()
        casePath = os.path.dirname(os.path.dirname(__file__))  # test_case目录下
        dataPath = os.path.dirname(casePath)
        self.file = dataPath + '\\data\\' + fileName

    def getDataPosVal(self):
        '''获取表格数据,字典形式保存,名称+行:(列,值)代表数据位置'''
        try:
            data = open_workbook(self.file)  # formatting_info=True保留数据格式
        except Exception as e:
            print(e, '获取%s文件失败' % self.file)
        table = data.sheets()[0]  # 通过索引获取第一张sheet表
        excelDict = OrderedDict()  # 创建一个有序的字典存放数据在第几行和对应值
        for row in range(table.nrows):
            rowsData = table.row_values(0)  # 读取第一行名称数据
            for col in range(table.ncols):
                excelDict[rowsData[col] + repr(row)] = [(row, col), table.cell(row, col).value]  # 多行数据显示
        return excelDict

    def creatExcel(self, posVal):
        '''创建一分相同数据表格替代原表格'''
        # posVal = self.getDataPosVal()
        # posVal['商品SKU1'][1] = '更改'
        wb = Workbook()
        ws = wb.add_sheet('Sheet11')
        for posVal in posVal.values():
            ws.write(posVal[0][0], posVal[0][1], posVal[1])  # row,col,value
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

    def InventoryNum(self):
        # 查询最近更新库存
        customerCode = self.consOderBy()
        proSku = self.consOderBy('product_sku', 'tbl_product')
        order = "select id from tbl_customer where customer_code='%s'" % customerCode
        self.cur.execute(order)
        cusId = self.cur.fetchone()[0]
        order = "select id from tbl_product where product_sku='%s'" % proSku
        self.cur.execute(order)
        proId = self.cur.fetchone()[0]
        order = "select storage from tbl_product_storage where customer_id='%s' and product_id='%s'" % (cusId, proId)
        self.cur.execute(order)
        stoNum = self.cur.fetchone()
        if stoNum is None:
            return 0
        return stoNum[0]

    def proStringNo(self, col, table):
        # 创建数据库不存在的字符串，如sku，支付单号等
        newData = self.consOderBy(col, table)  # 最新数据
        newStr = stringAddOne(newData)
        return newStr

    def proRecord(self, sku):
        # 商品备案
        order = "UPDATE tbl_product SET status=1 WHERE product_sku='%s';\
                 UPDATE tbl_product_message SET hg_status=40,ciq_status=40 WHERE product_id \
                 IN (SELECT id FROM tbl_product WHERE product_sku IN('%s'))" % (sku, sku)
        self.cur.execute(order)
        self.conn.commit()

    def __del__(self):
        self.conn.close()
        del self.conn


if __name__ == "__main__":
    a = postgreSql()
    print(a.proStringNo('product_sku', 'tbl_product'))
