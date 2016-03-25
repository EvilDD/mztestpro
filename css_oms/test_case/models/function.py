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


def stringAddOne(string):
    '''输入一个字符串,返回一个新的+1字符串'''
    num = re.search('\d*$', string).group(0)
    num = '0' if num == '' else num
    num = repr(int(num) + 1)
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
        newString = re.sub('\d*$', num, sku)
        return newString

    def __del__(self):
        self.conn.close()
        del self.conn


if __name__ == "__main__":
    a = postgreSql()
    print(a.proStringNo('product_sku', 'tbl_product'))
