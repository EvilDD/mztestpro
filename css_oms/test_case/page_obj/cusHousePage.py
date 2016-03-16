from .base import Bar
from time import sleep
from selenium.webdriver.common.by import By


class addWarehouse(Bar):
    '''客户管理->客户交货仓'''

    def iframe_page(self):
        '''进入客户交货仓的ifrme,点击新增'''
        sleep(0.8)  # 等待程序读取到所有一级菜单
        self.navigationBar('客户管理').click()
        self.driver.implicitly_wait(5)
        self.secondNavBar('客户交货仓').click()
        self.driver.switch_to.frame(self.switchIframe('客户交货仓'))

    # 进入新增客户交货仓界面,此界面是新增的窗口
    def newPage(self):
        self.buttonBar('新增').click()
        self.driver.switch_to.frame(self.switchIframe('添加客户交货仓'))

    # 客户代码
    def cusCode(self, code):
        self.find_element(By.NAME, 'cus_code').send_keys(code)

    # 电商平台
    def dspt(self, name):
        self.find_element(By.NAME, 'platform_name').send_keys(name)

    # 海关企业注册号
    def hgqyzch(self, code):
        self.find_element(By.NAME, 'hg_reg_no').send_keys(code)

    # 海关平台备案号
    def hgptbah(self, code):
        self.find_element(By.NAME, 'hg_platform_no').send_keys(code)

    # 海关企业备案号
    def hgqybah(self, code):
        self.find_element(By.NAME, 'hg_company_no').send_keys(code)

    # 商检平台备案号
    def sjptbah(self, code):
        self.find_element(By.NAME, 'ciq_platform_no').send_keys(code)

    # 商检企业备案号
    def sjqybah(self, code):
        self.find_element(By.NAME, 'ciq_company_no').send_keys(code)

    # 定位返回所有有下拉框选项的元素
    def optionBars(self):
        options = self.find_elements(By.CLASS_NAME, 'textbox-text-readonly')
        return options

    # 仓库选择
    def choiceWarehouse(self, warehouse):
        self.optionBars()[0].click()  # 点击弹出下拉
        self.selectOption(warehouse).click()  # 点击选取仓库

    # 海关接入方式
    def cusMod(self, mod):
        self.optionBars()[1].click()
        self.selectOption(mod).click()

    # 商检接入方式
    def ciqMod(self, mod):
        self.optionBars()[2].click()
        self.selectOption(mod).click()

    # 商品是否代备案
    def goodsRecord(self, text):
        self.optionBars()[3].click()
        self.selectOption(text).click()

    # 订单是否代备案
    def odersRecord(self, text):
        self.optionBars()[4].click()
        self.selectOption(text).click()

    # 填写海关和商检的ftp
    def ftpWrite(self, cus, ciq):
        cus, ciq = self.ftpContent(cus, ciq)
        self.find_element(By.NAME, 'hg_ftp_url').send_keys(cus[0])  # cus的ftp地址
        self.find_element(By.NAME, 'hg_ftp_account').send_keys(cus[1])  # cus的ftp帐号
        self.find_element(By.NAME, 'hg_ftp_password').send_keys(cus[2])  # cus的ftp密码

        self.find_element(By.NAME, 'ciq_ftp_url').send_keys(ciq[0])  # ciq的ftp地址
        self.find_element(By.NAME, 'ciq_ftp_account').send_keys(ciq[1])  # ciq的ftp帐号
        self.find_element(By.NAME, 'ciq_ftp_password').send_keys(ciq[2])  # ciq的ftp密码

    def selectOption(self, optionName):
        '''根据传入选项名字，自动选择'''
        options = {}
        sleep(0.8)
        optionEles = self.find_elements(By.CLASS_NAME, 'combobox-item')
        for optionEle in optionEles:
            options[optionEle.text] = optionEle
        return options[optionName]

    def ftpContent(self, cus, ciq):
        '''根据用户选择的海关商检方式填入对应ftp信息'''
        cus_ftp = []
        ciq_ftp = []
        ip = 'ftp://192.168.0.177:21'
        cus_ftp.append(ip)
        ciq_ftp.append(ip)
        if '元亨' in cus:
            cus_ftp.append('yuanheng')
            cus_ftp.append('yuanheng123')
        elif '口岸' in cus:
            cus_ftp.append('eport')
            cus_ftp.append('eport123')
        if '智检' in ciq:
            ciq_ftp.append('zhijian')
            ciq_ftp.append('zhijian123')
        elif '口岸' in ciq:
            ciq_ftp.append('eport')
            ciq_ftp.append('eport123')
        return cus_ftp, ciq_ftp

    # 添加客户交货仓保存流程
    def addCusWarehouse(self, newHouse):
        self.iframe_page()  # 切换到交货仓页面
        self.newPage()  # 切换到新增的页面
        self.cusCode(newHouse[0])
        self.choiceWarehouse(newHouse[1])
        self.cusMod(newHouse[2])
        self.ciqMod(newHouse[3])
        self.dspt(newHouse[4])
        self.hgqyzch(newHouse[5])
        self.hgptbah(newHouse[6])
        self.hgqybah(newHouse[7])
        self.sjptbah(newHouse[8])
        self.sjqybah(newHouse[9])
        self.goodsRecord(newHouse[10])
        self.odersRecord(newHouse[11])
        self.ftpWrite(newHouse[2], newHouse[3])
        self.buttonBar('保存').click()
