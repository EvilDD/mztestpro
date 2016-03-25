from .base import Bar
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from os.path import dirname


class addProucts(Bar):
    '''oms->商品管理->商品批量上传'''

    def iframe_page(self):
        '''进入商品上传ifrme'''
        self.secondNavBar('商品批量上传').click()  # 进入系统时商品管理页面已显示
        self.driver.switch_to.frame(self.switchIframe('商品批量上传'))

    # 浏览上传
    def fileUpload(self, filename):
        casePath = dirname(dirname(__file__))  # test_case目录下
        dataPath = dirname(casePath)
        filepath = dataPath + '\\data\\' + filename
        self.find_element(By.ID, 'fileUpload').send_keys(filepath)

    # 开始上传
    def startUpload(self):
        self.find_element(By.ID, 'batch-upload').click()

    # 确认上传
    def submit(self):
        self.find_element(By.ID, 'submit').click()

    # 取消上传
    def cancel(self):
        self.find_element(By.ID, 'cancel').click()

    # 上传入口
    def uploadLogin(self, filename):
        self.iframe_page()
        self.fileUpload(filename)
        self.startUpload()
        sleep(1)
        self.submit()
        # a = self.find_element(By.CLASS_NAME, 'btn-link')
        # ActionChains(self.driver).context_click(a).perform()

    # 信息提示
    def mesUpload(self):
        return self.find_element(By.CLASS_NAME, 'mess-content').text
