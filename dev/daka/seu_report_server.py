# -*- coding:utf-8 -*-
# NOW_VERSION S_1.1.1 (CLOUD)

import os
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def gettimestr():
    return time.strftime('%Y%m%d%H%M%S')


def pnl(text):
    with open('log/log_main.txt', 'a') as obj_file:
        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        writeinfo = time_str + '\t' + text + '\n'
        obj_file.write(writeinfo)
        obj_file.close()
    ptime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('[' + ptime + ']>>>>>>' + text)


def checkdone(text, browser):
    buttons = browser.find_elements_by_tag_name('button')
    for button in buttons:
        if button.get_attribute("textContent").find(text) >= 0:
            return True
    return False


def isTimeOver():
    ltime = time.localtime(time.time())
    h = ltime.tm_hour
    if h >= 15:
        return True
    else:
        return False


# 读取配置信息(默认'./config/all.cfg')
def load_config():
    config_return = {}
    try:
        with open('./config/all.cfg', 'r') as file:
            line_list = file.readlines()
            for line in line_list:
                if line.startswith('#') or line == '\n':
                    continue
                key = line.split('=*=')[0].strip()
                value = line.split('=*=')[1].strip()
                config_return[key] = value
        return config_return
    except FileNotFoundError:
        pnl('[WARNING] CANNOT LOAD CONFIG')
        with open('./config/all.cfg', 'w') as file:
            file.write('#THIS FILE IS TO CONFIG SEU_DAILY_REPORT\n'
                       '#ONLY AVAILABLE TO VERSION S_1.1.1\n'
                       '#PLEASE FILL ALL CONFIG IN CASE THAT PROGRAM MIGHT RUN IMPROPERLY\n'
                       '#COPYRIGHT CHIAKI AT SOUTHEAST UNIVERSITY, CHINA\n'
                       '\n'
                       '#Report Address\n'
                       'report_url =*= NULL\n'
                       '\n'
                       '#Webdriver Address\n'
                       'webdriver_addr =*= NULL\n'
                       '\n'
                       '#END OF CONFIG\n')
        pnl('[WARNING] WE HELPED YOU CREATE A NEW CONFIG')
        try:
            with open('./config/all.cfg', 'r') as file:
                line_list = file.readlines()
                for line in line_list:
                    if line.startswith('#') or line == '\n':
                        continue
                    key = line.split('=*=')[0].strip()
                    value = line.split('=*=')[1].strip()
                    config_return[key] = value
            return config_return
        except Exception as e:
            pnl('[ERROR] UNKNOWN ERROR(101): ' + str(e))
    except Exception as e:
        pnl('[ERROR] UNKNOWN ERROR(102): ' + str(e))


def make_report_all(_uid, _name, _username, _password):
    global report_url
    global webdriver_addr
    global chrome_config
    _uid = str(_uid)
    try:
        # 操作开始
        wd_point = webdriver.Chrome(webdriver_addr, options=chrome_config)
        wd_point.implicitly_wait(60)
        # 统一登录页面，寻找网页元素，填入信息，点击登录
        pnl(_uid + ': ' + _name + ' 登录统一身份认证...')
        wd_point.get(report_url)
        element_username = wd_point.find_element_by_id('username')  # Latest Update 2021-01-27
        element_password = wd_point.find_element_by_id('password')  # Latest Update 2021-01-27
        element_username.clear()
        element_password.clear()
        element_username.send_keys(_username)
        element_password.send_keys(_password)
        element_loginbutton = wd_point.find_element_by_class_name('auth_login_btn')  # Latest Update 2021-01-27
        element_loginbutton.submit()
        pnl(_uid + ': ' + _name + ' 容错等待...')
        time.sleep(20)  # 东大服务器老卡了
        # 进入打卡界面，确认是否打卡
        isDone = not checkdone("新增", wd_point)
        if isDone:
            pnl(_uid + ': ' + _name + ' 已完成任务(recount)')
            wd_point.quit()  # 非常重要！
            return
        else:
            # 元素正式操作
            pnl(_uid + ': ' + _name + ' 即将开始打卡...')
            time.sleep(1)
            pnl(_uid + ': ' + _name + ' 新增...')
            buttons = wd_point.find_elements_by_css_selector('button')
            for button in buttons:
                if button.get_attribute("textContent").find("新增") >= 0:
                    button.click()
                    # 根据用户数据输入体温
                    inputfileds = wd_point.find_elements_by_tag_name('input')
                    for i in inputfileds:
                        if i.get_attribute("placeholder").find("请输入当天晨检体温") >= 0:
                            pnl(_uid + ': ' + _name + ' 输入体温...')
                            i.click()
                            i.send_keys('36.5')  # 发送体温
                            time.sleep(3)
                            # 确认并提交
                            pnl(_uid + ': ' + _name + ' 尝试提交...')
                            buttons = wd_point.find_elements_by_tag_name('button')
                            for button in buttons:
                                if button.get_attribute("textContent").find("确认并提交") >= 0:
                                    button.click()
                                    buttons = wd_point.find_elements_by_tag_name('button')
                                    button = buttons[-1]
                                    time.sleep(3)
                                    pnl(_uid + ': ' + _name + ' 提交中...')
                                    # 提交
                                    if button.get_attribute("textContent").find("确定") >= 0:
                                        button.click()
                                        pnl(_uid + ': ' + _name + '于 ' + gettimestr() + ' 成功打卡！')
                                    else:
                                        pnl('[ERROR]' + _uid + ': ' + _name + ' WARNING:OLD_VERSION_ERROR_1')
                                    break
                            break
                    break
            wd_point.quit()  # 重要的
            return
    except Exception as e:
        pnl('[WARNING]' + _uid + _name + ' 打卡失败')


if __name__ == '__main__':
    pnl('STARTFLAG = NOW_VERSION S_1.1.1')
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
    # 创建目录，如果不存在
    if not os.path.exists("log"):
        os.mkdir("log")
    if not os.path.exists("encdata"):
        os.mkdir("encdata")
    if not os.path.exists("config"):
        os.mkdir("config")
    # 读取设置
    config_dict = load_config()
    report_url = config_dict['report_url']
    webdriver_addr = config_dict['webdriver_addr']
    if report_url == 'NULL' or webdriver_addr == 'NULL':
        raise Exception('[ERROR]invalid report url or webdriver addr')

    # 多线程打卡
    while True:
        time_is_over = isTimeOver()
        if time_is_over:
            pnl('Timeover, try 1 hour later')
            time.sleep(3600)
            continue
        icounter = 0
        with open('encdata/userlist.json') as file:
            all_user_data = file.readline()
            all_user_data_list = json.loads(all_user_data)
            file.close()

        while icounter < len(all_user_data_list):
            uid = all_user_data_list[icounter]['uid']
            name = all_user_data_list[icounter]['name']
            username = all_user_data_list[icounter]['username']
            password = all_user_data_list[icounter]['password']
            make_report_all(uid, name, username, password)
            icounter += 1
        pnl('A circle mission has done, sleep 2h')
        time.sleep(7200)
