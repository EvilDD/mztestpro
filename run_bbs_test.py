from HTMLTestRunner import HTMLTestRunner
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from allcase_list import allTestNames
import smtplib
import unittest
import time
import os


# 定义发送邮件
def send_mail(file_new):
    # 创建一个附件实例
    msg = MIMEMultipart()
    # 构造附件
    att = MIMEText(open(file_new, 'rb').read(), 'base64', 'utf-8')
    att["Content-Type"] = "application/octet-stream"
    att["Content-Disposition"] = 'attachment;filename="testReult.html"'  # 任意邮件中显示的文件名
    msg.attach(att)
    # 构造内容
    text = MIMEText("大家好,\n本邮件由系统自动发送,\n附件为这次自动化测试报告的结果, 请下载后查看!\n源码: https://github.com/EvilDD (mztestpro项目)")
    msg.attach(text)
    # 加邮件头
    msgTos = (
        '243435508@qq.com',
        'yadong.zhou@56100.com',
        '1992349278@qq.com',
        '447959115@qq.com'
    )
    msg['from'] = 'zydsyu@sina.cn'
    msg['subject'] = '【测试报告】自动化测试报告'

    # 发邮件
    try:
        server = smtplib.SMTP()
        server.connect('smtp.sina.cn')
        password = input("输入邮箱密码:")
        server.login('zydsyu@sina.cn', password)
        for msgTo in msgTos:
            print(msgTo)
            server.sendmail(msg['from'], msgTo, msg.as_string())
        server.quit()
    except Exception as e:
        print(e)


# 查找最新生成的测试报告
def new_report(testreport):
    lists = os.listdir(testreport)
    lists.sort(key=lambda f: os.path.getmtime(testreport + "\\" + f))  # f为lists中的元素,sort是排序
    file_new = os.path.join(testreport, lists[-1])
    return file_new

if __name__ == '__main__':
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    filename = './css_oms/report/' + now + 'result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='清关系统',
                            description='环境：win8,浏览器：chrome'
                            )
    # discover = unittest.defaultTestLoader.discover('./css_oms/test_case', pattern='*_css.py')  # 无序运行
    testunit = unittest.TestSuite()
    for testcase in allTestNames:
        testunit.addTest(unittest.makeSuite(testcase))
    runner = unittest.TextTestRunner()

    runner.run(testunit)
    fp.close()
    file_path = new_report('./css_oms/report/')
    # send_mail(file_path)
