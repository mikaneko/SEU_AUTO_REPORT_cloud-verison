from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import fc  # functionCollection
import cpi  # copyrightInfo
import myFunction

import time
import json
import os

# 程序信息
projectId = "auto_report.chiaki.grp"
projectAuthor = "atarashi chiaki"
projectName = "东南大学每日健康打卡（工业版）"
projectVersion = "INDUSTRY VERSION 2"
projectReleaseTime = "2021-01-31"
# print程序头
cpi.versionUpdateInfo()
fc.printTips()
# 创建各种目录
if not os.path.exists("./log"):
    os.mkdir("./log")
if not os.path.exists("./encdata"):
    os.mkdir("./encdata")
if not os.path.exists("./config"):
    os.mkdir("./config")
# 日志文件和配置文件保存目录（默认）
log_relative_addr = "./log/log_main.txt"
config_relative_addr = "./config/config_main.json"
userdata_relative_addr = "./encdata/userlist.json"
# 欢迎界面
programStartingTime = fc.stdTimeStr()
fc.printBasicInfo(projectId, projectName, projectVersion, projectReleaseTime, programStartingTime)
fc.logBasicInfoDefault(projectId, projectName, projectVersion, projectReleaseTime, programStartingTime)
# 设置chrome启动参数
chrome_config = Options()
chrome_config.add_argument('--no-sandbox')  # root权限下跑
chrome_config.add_argument('–-disable-dev-shm-usage')  # 大量渲染时候写入/tmp而非/dev/shm
chrome_config.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_config.add_argument('--start-maximized')  # 最大化启动
chrome_config.add_argument('--incognito')  # 无痕隐身模式
chrome_config.add_argument('disable-cache')  # 禁用缓存
chrome_config.add_argument('disable-infobars')  # 去掉浏览器默认的“chrome正受到自动测试软件的控制”信息栏显示
chrome_config.add_argument('--headless')  # 无头模式
chrome_config.add_experimental_option('excludeSwitches', ['enable-logging'])  # 不显示黑error

# （1）将config载入
var_configdata_temp = myFunction.get_config_main()
var_configdata = json.loads(str(var_configdata_temp).strip())
var_chromedriverlink = var_configdata['chrome_driver_link']
var_website = var_configdata['web_link']
var_temperature = var_configdata['temperature']

while True:
    print('-'*50)
    print('>>main program operation')
    print('  (1)run the program')
    print('  (2)manage user')
    print('  (3)list user log(暂时不可用)')
    main_operation = input('>>INPUT: operation code:  ')
    if main_operation == '1':
        break
    elif main_operation == '2':
        myFunction.manage_userlist_main()
    elif main_operation == '3':
        myFunction.print_user_log()
    else:
        print('>>wrong operation, try again')


# 开始每日打卡咯
while True:
    time_is_over = fc.isTimeOver()
    if time_is_over:
        fc.printAndLogDefault('Timeover, try 1 hour later')
        time.sleep(3600)
        continue
    with open('./encdata/userlist.json') as file:
        all_user_data = file.readline()
        all_user_data_list = json.loads(all_user_data)
        file.close()
    icounter = 0
    while icounter < len(all_user_data_list):
        iuid = all_user_data_list[icounter]['uid']
        iname = all_user_data_list[icounter]['name']
        iusernum = all_user_data_list[icounter]['usernum']
        ipassword = all_user_data_list[icounter]['password']
        try:
            # 操作开始
            wd_point = webdriver.Chrome(var_chromedriverlink, options=chrome_config)
            wd_point.implicitly_wait(60)
            # 统一登录页面，寻找网页元素，填入信息，点击登录
            fc.printAndLogDefault(iname + ' 正在尝试登录统一身份认证...')
            wd_point.get(var_website)
            element_usernum = wd_point.find_element_by_id('username')  # Latest Update 2021-01-27
            element_password = wd_point.find_element_by_id('password')  # Latest Update 2021-01-27
            element_usernum.clear()
            element_password.clear()
            element_usernum.send_keys(iusernum)
            element_password.send_keys(ipassword)
            element_loginbutton = wd_point.find_element_by_class_name('auth_login_btn')  # Latest Update 2021-01-27
            element_loginbutton.submit()
            fc.printAndLogDefault('由于东大服务器卡顿，需要一定时间的等待(about 20s)...')
            time.sleep(20)  # 东大服务器老卡了
            # 进入打卡界面，确认是否打卡
            buttons = wd_point.find_elements_by_tag_name('button')
            isDone = not fc.check("新增", wd_point)
            if isDone:
                fc.printAndLogDefault(fc.getDateStr() + ' ' + iname + ' 已经打完卡')
                wd_point.quit()  # 非常重要！
                icounter += 1  # 非常重要！
                continue
            else:
                # 元素正式操作
                fc.printAndLogDefault(iname + ' 即将开始打卡...')
                fc.printAndLogDefault(iname + ' 正在尝试新增...')
                buttons = wd_point.find_elements_by_css_selector('button')
                for button in buttons:
                    if button.get_attribute("textContent").find("新增") >= 0:
                        button.click()
                        # 根据用户数据输入体温
                        inputfileds = wd_point.find_elements_by_tag_name('input')
                        for i in inputfileds:
                            if i.get_attribute("placeholder").find("请输入当天晨检体温") >= 0:
                                fc.printAndLogDefault(iname + ' 正在尝试输入体温...')
                                i.click()
                                i.send_keys(var_temperature)  # 发送体温
                                time.sleep(3)
                                # 确认并提交
                                fc.printAndLogDefault(iname + ' 正在尝试提交...')
                                buttons = wd_point.find_elements_by_tag_name('button')
                                for button in buttons:
                                    if button.get_attribute("textContent").find("确认并提交") >= 0:
                                        button.click()
                                        buttons = wd_point.find_elements_by_tag_name('button')
                                        button = buttons[-1]
                                        time.sleep(3)
                                        fc.printAndLogDefault(iname + ' 提交...')
                                        # 提交
                                        if button.get_attribute("textContent").find("确定") >= 0:
                                            button.click()
                                            isDone = True  # 标记已完成打卡
                                            fc.printAndLogDefault('于 '+fc.getDateStr() + ' ' + iname + ' 成功打卡！')
                                        else:
                                            fc.printAndLogDefault(iname + ' WARNING:OLD_VERSION_ERROR_1')
                                        break
                                break
                        break
                wd_point.quit()  # 非常重要！
                icounter += 1
        except:
            print('[WARNING]'+iname + ' 打卡失败！')
    fc.printAndLogDefault('All users has done mission (sleep 2h)')
    time.sleep(7200)
    continue
# Done
