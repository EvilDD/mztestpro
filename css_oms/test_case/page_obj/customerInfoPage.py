from .base import Bar
from time import sleep
from selenium.webdriver.common.by import By


class cusInfo(Bar):
    '''客户管理->客户资料界面'''

    def iframe_page(self):
        '''进入客户资料的ifrme,点击新增'''
        sleep(0.5)  # 等待程序读取到所有一级菜单
        self.navigationBar('客户管理').click()
        self.driver.implicitly_wait(5)
        self.secondNavBar('客户资料').click()
        self.driver.switch_to.frame(self.switchIframe('客户资料'))

    def newPage(self):
        self.buttonBar('新增').click()

    # 客户代码
    def cusCode(self):
        customerCode = self.find_element(By.NAME, 'customer_code').get_attribute('value')
        return customerCode

    # 客户名称
    def cusName(self, name):
        self.find_element(By.NAME, 'customer_name').send_keys(name)

    # 登录密码
    def cusPw(self, password):
        self.find_element(By.NAME, 'login_pwd').send_keys(password)

    # 联系电话
    def tel(self, telphone):
        self.find_element(By.NAME, 'tel').send_keys(telphone)

    # 传真
    def fax(self, fax):
        self.find_element(By.NAME, 'fax').send_keys(fax)

    # 邮箱
    def mail(self, mail):
        self.find_element(By.NAME, 'email').send_keys(mail)

    # 单位名称
    def company(self, com):
        self.find_element(By.NAME, 'company_name').send_keys(com)

    # 单位编号
    def comSn(self, sn):
        self.find_element(By.NAME, 'company_sn').send_keys(sn)

    # 组织机构代码
    def orgCode(self, code):
        self.find_element(By.NAME, 'org_code').send_keys(code)

    # 网站域名
    def web(self, web):
        self.find_element(By.NAME, 'domain_name').send_keys(web)

    # 新增客户主流程
    def add_customer(self, newCus):
        self.iframe_page()
        self.newPage()
        self.cusName(newCus[0])
        self.cusPw(newCus[1])
        self.tel(newCus[2])
        self.fax(newCus[3])
        self.mail(newCus[4])
        self.company(newCus[5])
        self.comSn(newCus[6])
        self.orgCode(newCus[7])
        self.web(newCus[8])
        self.buttonBar('保存').click()

    newCus_loc = (By.ID, 'datagrid-row-r2-2-0')
    newCusCode_loc = (By.CLASS_NAME, 'datagrid-cell-c2-customer_code')
    error_hint_loc = (By.CLASS_NAME, 'mess-content')

    # 选择最新的一个客户
    def choiceCustomer(self):
        self.find_element(*self.newCus_loc).click()

    # 点击禁用
    def forbidden(self):
        self.buttonBar('禁用').click()

    # 确认禁用
    def comfirm(self):
        self.buttonBar('确定').click()

    # 禁用客户流程
    def forbiCustomer(self):
        self.iframe_page()
        sleep(0.5)
        self.choiceCustomer()
        self.forbidden()
        self.comfirm()

    # 返回刚禁用客户的代码
    def offCusCode(self):
        code = self.find_element(*self.newCus_loc).find_element(*self.newCusCode_loc).text
        return code

    # 提示客户被禁用错误
    def customer_off_error(self):
        return self.find_element(*self.error_hint_loc).text

    def using(self):
        self.buttonBar('启用').click()
