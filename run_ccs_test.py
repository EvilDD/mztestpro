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
    text = MIMEText("大家好,\n本邮件由系统自动发送,\n附件为这次自动化测试报告的结果, 请下载后查看!\n源码分享: https://github.com/EvilDD (mztestpro项目)")
    msg.attach(text)
    # 加邮件头
    msgTos = (
        '996758689@qq.com',
        '447959115@qq.com',
        'yadong.zhou@56100.com',
        '243435508@qq.com',
    )  # 发送地址
    msg['to'] = ';'.join(msgTos)  # 收件栏显示
    msg['from'] = 'zydsyu@sina.cn'  # 发件栏显示
    msg['subject'] = '【测试报告】自动化测试报告'

    # 发邮件
    try:
        server = smtplib.SMTP()
        server.connect('smtp.sina.cn')
        password = input("输入邮箱密码:")
        server.login('zydsyu@sina.cn', password)
        server.sendmail(msg['from'], msgTos, msg.as_string())
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
                            title='清关系统简略测试',
                            description='环境：win8,浏览器：chrome'
                            )
    # runner = unittest.TextTestRunner()

    # discover = unittest.defaultTestLoader.discover('./css_oms/test_case', pattern='*_css.py')  # 无序运行
    testunit = unittest.TestSuite()
    for testcase in allTestNames:
        testunit.addTest(unittest.makeSuite(testcase))

    runner.run(testunit)
    fp.close()
    file_path = new_report('./css_oms/report/')
    send_mail(file_path)
