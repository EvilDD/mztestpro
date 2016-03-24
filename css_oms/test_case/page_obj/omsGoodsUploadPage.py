from .base import Bar
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class addProucts(Bar):
    '''oms->商品管理->商品批量上传'''

    def iframe_page(self):
        '''进入商品上传ifrme'''
        self.secondNavBar('商品批量上传').click()  # 进入系统时商品管理页面已显示
        self.driver.switch_to.frame(self.switchIframe('商品批量上传'))

    def download(self):
        self.iframe_page()
        a = self.find_element(By.CLASS_NAME, 'btn-link')
        ActionChains(self.driver).context_click(a).perform()
