from selenium import webdriver
import os
import csv
import psycopg2


def insert_img(driver, file_name):
    '''截图函数'''
    base_dir = os.path.dirname(os.path.dirname(__file__))  # test_case目录下
    base_dir = base_dir.replace('\\', '/')
    base = base_dir.split('/test_case')[0]  # test_case上级目录
    file_path = base + '/report/image/' + file_name
    # print(file_path)
    driver.get_screenshot_as_file(file_path)  # 截屏


def add_csv_datas(csvname, csvrow):
    # dataPath = os.path.dirname(path)  # 获取当前路径上级目录
    csvPath = run_path + '\\data\\' + csvname
    rows = []
    with open(csvPath, 'r') as csvFile:
        datas = csv.reader(csvFile)
        for row in datas:
            rows.append(row)
    return rows[csvrow][1]


class postgreSql:
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

    def __del__(self):
        self.conn.close()
        del self.conn


if __name__ == "__main__":
    # driver = webdriver.Chrome()
    # driver.get("http://www.baidu.com")
    # insert_img(driver, 'baidu.jpg')
    # driver.quit()
    a = postgreSql()
    print(type(a.consOderBy('product_sku', 'tbl_product')))
