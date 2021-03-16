from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import fc  # functionCollection
import cpi # copyrightInfo

import time
import json
import os
import random

# 程序信息
projectId = "auto_report.chiaki.obj"
projectAuthor = "atarashi chiaki"
projectName = "东南大学每日健康打卡（个人自动版）"
projectVersion = "0.2.2"
projectReleaseTime = "2021-01-28"

# print程序头
cpi.versionUpdateInfo()
fc.printTips()
# 创建各种目录
if not os.path.exists("./log"):
    os.mkdir("./log")
if not os.path.exists("./userdata"):
    os.mkdir("./userdata")
if not os.path.exists("./config"):
    os.mkdir("./config")
# 日志文件和配置文件保存目录（默认）
log_relative_addr = "./log/log_main.txt"
config_relative_addr = "./config/config_main.config"
#（1）将config载入
var_configdata_temp = fc.loadConfigDataDefault()
var_configdata = json.loads(str(var_configdata_temp).strip())
var_chromedriverlink = var_configdata['chrome_driver_link']
var_website = var_configdata['school_website_link']
#（2）将userdata载入
var_userdata_temp = fc.loadUserdataDefault()
var_userdata = json.loads(str(var_userdata_temp).strip())
var_username = var_userdata['usernum']
var_password = var_userdata['password']
var_location = var_userdata['location']
var_min_temperature = var_userdata['min_temperature']
var_max_temperature = var_userdata['max_temperature']
# 更新变量
var_min_temperature_int = int(float(var_min_temperature)*10)
var_max_temperature_int = int(float(var_max_temperature)*10)
random_temperature = (random.randint(var_min_temperature_int,var_max_temperature_int)/10.0)
random_temperature_str = str(random_temperature)
website = var_website
isDone = False
timeOver = False
programStartingTime = fc.stdTimeStr()
# 欢迎界面
fc.printBasicInfo(projectId,projectName,projectVersion,projectReleaseTime,programStartingTime)
fc.logBasicInfoDefault(projectId,projectName,projectVersion,projectReleaseTime,programStartingTime)
# 设置chrome启动参数
chrome_config = Options()
chrome_config.add_argument('--no-sandbox') # root权限下跑
chrome_config.add_argument('–-disable-dev-shm-usage') # 大量渲染时候写入/tmp而非/dev/shm
chrome_config.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_config.add_argument('--start-maximized')  # 最大化启动
chrome_config.add_argument('--incognito')  # 无痕隐身模式
chrome_config.add_argument('disable-cache')  # 禁用缓存
chrome_config.add_argument('disable-infobars') # 去掉浏览器默认的“chrome正受到自动测试软件的控制”信息栏显示
chrome_config.add_argument('--headless')  # 无头模式
chrome_config.add_experimental_option('excludeSwitches', ['enable-logging'])#不显示黑error
# 开始咯
while True:
    # 获取时间
    timeOver = fc.isTimeOver()
    # 当前时间超过打卡时间，不予执行，循环直到时间满足要求
    if timeOver :
        fc.logDefault('时间未达要求,sleep1800')
        time.sleep(1800)
        continue
    # 当前时间满足要求，登录并检查是否需要打卡
    wd_point = webdriver.Chrome(var_chromedriverlink,options=chrome_config)
    wd_point.implicitly_wait(60)
    #统一登录页面，寻找网页元素，填入信息，点击登录
    fc.printAndLogDefault('正在尝试登录统一身份认证...')
    wd_point.get(website)
    element_usernum = wd_point.find_element_by_id('username') # Latest Update 2021-01-27
    element_password = wd_point.find_element_by_id('password') # Latest Update 2021-01-27
    element_usernum.clear()
    element_password.clear()
    element_usernum.send_keys(var_username)
    element_password.send_keys(var_password)
    element_loginbutton = wd_point.find_element_by_class_name('auth_login_btn') # Latest Update 2021-01-27
    element_loginbutton.submit()
    fc.printAndLogDefault('由于东大服务器卡顿，需要一定时间的等待(about 20s)...')
    time.sleep(20) #东大服务器老卡了
    #进入打卡界面，确认是否打卡
    buttons = wd_point.find_elements_by_tag_name('button')
    isDone = not fc.check("新增",wd_point)
    if isDone:
        fc.printAndLogDefault(fc.getDateStr()+' 已经打完卡')
        fc.printAndLogDefault('下次打卡检查时间为1小时后...')
        isDone = False
        timeOver = False
        wd_point.quit()
        time.sleep(3600)
        continue
    else:
        fc.printAndLogDefault('即将开始打卡...')
        fc.printAndLogDefault('尝试点击新增按钮...')
        buttons = wd_point.find_elements_by_css_selector('button')
        for button in buttons:
            if button.get_attribute("textContent").find("新增") >= 0:
                button.click()
                # 根据用户数据输入体温
                inputfileds = wd_point.find_elements_by_tag_name('input')
                for i in inputfileds:
                    if i.get_attribute("placeholder").find("请输入当天晨检体温") >= 0:
                        fc.printAndLogDefault('正在尝试输入体温...')
                        i.click()
                        i.send_keys(random_temperature_str)# 发送体温
                        time.sleep(3)
                        # 确认并提交
                        fc.printAndLogDefault('正在尝试提交...')
                        buttons = wd_point.find_elements_by_tag_name('button')
                        for button in buttons:
                            if button.get_attribute("textContent").find("确认并提交") >= 0:
                                button.click()
                                buttons = wd_point.find_elements_by_tag_name('button')
                                button = buttons[-1]
                                time.sleep(3)
                                fc.printAndLogDefault('提交...')
                                # 提交
                                if button.get_attribute("textContent").find("确定") >= 0:
                                    button.click()
                                    isDone = True  # 标记已完成打卡
                                    fc.printAndLogDefault('完成打卡，在'+fc.getDateStr())
                                else:
                                    fc.printAndLogDefault('WARNING:OLD_VERSION_ERROR_1')
                                break
                        break
                break
        wd_point.quit()
        fc.printAndLogDefault('下次打卡检查时间为1小时后...')
        time.sleep(3600)
        continue
# 循环代码
