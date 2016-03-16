from selenium.webdriver.common.by import By
from .base import Page
from time import sleep


class csslogin(Page):
    '''css用户登录界面'''

    url = '/admin'  # css地址

    # 元素参数
    css_login_user_loc = (By.ID, 'username')
    css_login_pw_loc = (By.ID, 'un')
    css_login_wh_loc = (By.XPATH, '//div[@class="logtxt dropdown"]/input')  # 仓库

    # 返回要选择仓库的loc
    def wh_choice(self, warehouse):
        self.find_element(*self.css_login_wh_loc).click()
        self.driver.implicitly_wait(3)  # 等待隐藏的仓库选项
        return (By.LINK_TEXT, warehouse)

    css_login_captcha_loc = (By.NAME, 'captcha')
    css_login_button_loc = (By.CLASS_NAME, 'btn-login')

    # 登录用户名
    def login_username(self, username):
        self.find_element(*self.css_login_user_loc).send_keys(username)

    # 登录密码
    def login_password(self, password):
        self.find_element(*self.css_login_pw_loc).send_keys(password)

    # 登录仓库
    def login_wh(self, warehouse):
        css_login_wh_choice_loc = self.wh_choice(warehouse)
        self.find_element(*css_login_wh_choice_loc).click()

    # 登录验证码
    def login_captcha(self, captcha):
        self.find_element(*self.css_login_captcha_loc).send_keys(captcha)

    # 登录按钮
    def login_button(self):
        self.find_element(*self.css_login_button_loc).click()

    # 统一登录入口
    def admin_login(self, username='admin', password='123123', warehouse='广州白云---GZBY', captcha='zyd'):
        self.open()
        sleep(0.3)  # 防止偶尔admin输入不成功
        self.login_username(username)
        self.login_password(password)
        self.login_wh(warehouse)
        self.login_captcha(captcha)
        self.login_button()

    error_hint_loc = (By.CLASS_NAME, 'mess-content')

    # 验证码错误
    def captcha_error_hint(self):
        return self.find_element(*self.error_hint_loc).text

    # 用户名错误
    def user_error_hint(self):
        return self.find_element(*self.error_hint_loc).text

    # 密码错误
    def pw_error_hint(self):
        return self.find_element(*self.error_hint_loc).text

    # 登录成功,用户名一致
    def user_login_suc(self):
        sleep(0.3)  # 防止登录成功浏览器没跳转过来
        username = self.find_element(*(By.XPATH, '/html/body/div[1]/div/div/div[2]/span')).text
        username = username.strip('您好： ')
        return username

    # 登录成功,仓库一致
    def warehouse_login_suc(self):
        warehouse = self.find_element(*(By.XPATH, '/html/body/div[1]/div/div/div[2]/a[3]')).text
        return warehouse


class omslogin(Page):
    """oms用户登录界面"""
    url = '/'
    # 元素参数
    css_login_user_loc = (By.ID, 'username')
    css_login_pw_loc = (By.ID, 'un')
    css_login_captcha_loc = (By.NAME, 'captcha')
    css_login_button_loc = (By.CLASS_NAME, 'btn-login')

    # 登录用户名
    def login_username(self, username):
        self.find_element(*self.css_login_user_loc).send_keys(username)

    # 登录密码
    def login_password(self, password):
        self.find_element(*self.css_login_pw_loc).send_keys(password)

    # 登录验证码
    def login_captcha(self, captcha):
        self.find_element(*self.css_login_captcha_loc).send_keys(captcha)

    # 登录按钮
    def login_button(self):
        self.find_element(*self.css_login_button_loc).click()

    # 统一登录入口
    def customer_login(self, username='admin', password='123123',  captcha='zyd'):
        self.open()
        sleep(0.3)  # 防止偶尔admin输入不成功
        self.login_username(username)
        self.login_password(password)
        self.login_captcha(captcha)
        self.login_button()
