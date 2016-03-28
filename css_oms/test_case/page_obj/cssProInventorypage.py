from .base import Bar
from time import sleep
from selenium.webdriver.common.by import By
from os.path import dirname
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class inventPage(Bar):
    '''css客户库存管理'''

    def iframe_page(self):
        '''进入商品管理->库存管理'''
        sleep(0.8)
        self.navigationBar('商品管理').click()
        self.driver.implicitly_wait(5)
        self.secondNavBar('库存管理').click()
        self.driver.switch_to.frame(self.switchIframe('库存管理'))

    # 选择文件上传
    def selDoc(self, filename):
        casePath = dirname(dirname(__file__))  # test_case目录下
        dataPath = dirname(casePath)
        filepath = dataPath + '\\data\\' + filename
        self.find_element(By.ID, 'fileUpload').send_keys(filepath)

    # 确认上传
    def submit(self):
        self.find_element(By.ID, 'submit').click()

    # 全部选择
    def selAll(self):
        self.find_element(By.CLASS_NAME, 'datagrid-header-check').click()

    # 等待上传成功后第一列数据出现
    def waitDisplay(self):
        WebDriverWait(self.driver, 30, 0.5).until(EC.element_to_be_clickable((By.ID, 'datagrid-row-r4-2-0')))

    # 等待第一条验证信息出现
    def waitDisable(self):
        WebDriverWait(self.driver, 30, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="datagrid-row-r4-2-0"]/td[7]/div/span')))

    # 库存上传入口
    def inventoryUpload(self, filename):
        self.iframe_page()
        self.selDoc(filename)
        self.submit()
        self.waitDisplay()
        self.selAll()
        self.buttonBar('提交').click()
        self.waitDisable()
        self.buttonBar('返回').click()
