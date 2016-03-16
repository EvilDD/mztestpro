from selenium.webdriver import Remote
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def browser():
    '''启动浏览器'''
    # dcap = dict(DesiredCapabilities.PHANTOMJS)
    # dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) ""Gecko/20100101 Firefox/25.0")
    # driver = webdriver.PhantomJS()

    driver = webdriver.Chrome()

    # host = '127.0.0.1:4444'  # 运行主机：默认端口号
    # dc = {'browserName': 'chrome'}  # 指定浏览器(火狐)
    # driver = Remote(command_executor='http://' + host + '/wd/hub', desired_capabilities=dc)
    return driver

if __name__ == '__main__':
    dr = browser()
    dr.get("http://www.baidu.com")
    dr.quit()
