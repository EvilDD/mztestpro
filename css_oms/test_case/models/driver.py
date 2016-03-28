from selenium.webdriver import Remote
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def browser():
    '''启动浏览器'''
    # driver = webdriver.PhantomJS()
    driver = webdriver.Firefox()
    # driver = webdriver.Chrome()

    host = '127.0.0.1:4444'  # 运行主机：默认端口号
    dc = {'browserName': 'phantomjs'}  # 指定浏览器(火狐),安装默认路径解决
    # driver = Remote(command_executor='http://' + host + '/wd/hub', desired_capabilities=dc)
    return driver

if __name__ == '__main__':
    dr = browser()
    dr.get("http://www.baidu.com")
    dr.quit()


# lists = {
#     'http://127.0.0.1:4444/wd/hub': 'firefox',
#     'http://127.0.0.1:5555/wd/hub': 'internet explorer',
#     'http://127.0.0.1:5556/wd/hub': 'chrome',
# }
# for host, browser in lists.items():
#     print(host, browser)
#     driver = Remote(command_executor=host,
#                     desired_capabilities={
#                         "browserName": browser,
#                         "version": "",
#                         "platform": "ANY",
#                         "javascriptEnabled": True,
#                     }
#                     )
