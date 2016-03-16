from selenium.webdriver.common.by import By
# from .base import urls
'''各界面的url存放'''
urls = {
    '首页': 'http://zydong.newoms.com/admin/panel/index',
    '欢迎使用': 'http://zydong.newoms.com/admin/panel/welcome',
    '客户资料': 'http://zydong.newoms.com/admin/customer/customerData',
    '客户API': 'http://zydong.newoms.com/admin/customer/customerAPI',
    '客户交货仓': 'http://zydong.newoms.com/admin/customer/payWarehouse',
    '添加客户交货仓': 'http://zydong.newoms.com/admin/customer/addPayWarehouse'
}


class Page(object):
    """页面基础类,用于所有页面的继承"""

    oms_url = 'http://zydong.newoms.com'
    # css_url = 'http://zydong.newoms.com/admin'

    def __init__(self, selenium_driver, base_url=oms_url, parent=None):
        self.base_url = base_url
        self.driver = selenium_driver
        self.timeout = 30
        self.parent = parent

    def _open(self, url):
        url = self.base_url + url
        self.driver.get(url)
        assert self.on_page()  # 判断当前页面是否已经加载成功

    def open(self):
        self._open(self.url)

    def on_page(self):
        return self.driver.current_url == (self.base_url + self.url)

    def find_element(self, *loc):
        return self.driver.find_element(*loc)

    def find_elements(self, *loc):
        return self.driver.find_elements(*loc)

    def script(self, src):
        return self.driver.execute_script(src)


class Bar(Page):

    def navigationBar(self, barName):
        menusName = {}  # 一级导航菜单按钮
        menus = self.find_elements(By.CLASS_NAME, 'panel-title')
        for menu in menus:
            menusName[menu.text] = menu
            # print(menu.text)
        return menusName[barName]

    def secondNavBar(self, barName):
        menusName = {}  # 二级导航菜单按钮
        menus = self.find_elements(By.CLASS_NAME, 'nav')
        for menu in menus:
            if menu.text != '':
                menusName[menu.text] = menu
        return menusName[barName]

    '''智能返回一个iframe的定位'''

    def switchIframe(self, iframeName):
        # 初步预计打开2个iframe,并保存iframe的url作为key和定位元素作为值
        iframes = {}
        self.driver.switch_to.default_content()  # 每次查找前先退出当前iframe
        for i in range(2):
            xpath = '/html/body/div[4]/div/div/div[2]/div[' + repr(i + 1) + ']/div/iframe'
            try:
                Src = self.find_element(By.XPATH, xpath).get_attribute('src')
                Name = self.find_element(By.XPATH, xpath)
                iframes[Src] = Name
            except:
                pass
        # 通过setting中的urls字典的values找到key
        key_list = []
        value_list = []
        for key, value in urls.items():
            key_list.append(key)
            value_list.append(value)
        # print('---' + iframeName)
        if iframeName in key_list:
            index = key_list.index(iframeName)
            iframeSrc = value_list[index]
            # print(iframeSrc + '---')
            if iframeSrc in iframes.keys():
                return iframes[iframeSrc]
            else:
                print('不存在' + iframeName + '的iframe')
                return False
        else:
            print('给的iframe名字在setting的url中无匹配')

    def buttonBar(self, barName):
        buttonName = {}  # frame页面中的小按钮
        buttons = self.find_elements(By.CLASS_NAME, 'l-btn-text')
        for button in buttons:
            if button.text != ' ':
                buttonName[button.text] = button
                # print(button.text)
        return buttonName[barName]
