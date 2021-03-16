import time
import json

# 读取登录信息(默认：'./userdata/userdata.json')
def loadUserdataDefault():
    try:
        with open("./userdata/userdata.json",'r') as obj_file:
            input_data_str = obj_file.readline()
            obj_file.close()
            print(">>已读取userdata")
    except:
        print(">>未发现./userdata/userdata.json")
        print(">>即将引导你设置userdata...")
        time.sleep(5)
        with open("./userdata/userdata.json",'w') as obj_file:
            usernum=input(">>>输入：一卡通号：  ")
            password=input(">>>输入：密码：  ")
            location=""
            min_temperature = input(">>>输入：最低体温：  ")
            max_temperature = input(">>>输入：最高体温：  ")
            input_data={"usernum":usernum,
                        "password":password,
                        "location":" ",
                        "min_temperature":min_temperature,
                        "max_temperature":max_temperature}
            input_data_str=json.dumps(input_data)+'\n'
            obj_file.write(input_data_str)
            obj_file.close()

    return input_data_str

# 读取配置信息(默认'./config/config_main.config')
def loadConfigDataDefault():
    try:
        with open("./config/config_main.config",'r') as obj_file:
            input_config_str = obj_file.readline()
            obj_file.close()
            print(">>已读取config_main")
    except:
        print(">>未发现./config/config_main.config")
        print(">>即将引导你设置config_main...")
        time.sleep(5)
        with open("./config/config_main.config",'w') as obj_file:
            chrome_driver_link = input(">>>输入：chromedriver地址：  ")
            school_website_link = input(">>>输入：每日打卡地址：  ")
            input_config = {"chrome_driver_link":chrome_driver_link,
                            "school_website_link":school_website_link}
            input_config_str = json.dumps(input_config)+'\n'
            obj_file.write(input_config_str)
            obj_file.close()

    return input_config_str

# 打印输出，并写入日志(默认'./log/log_main.txt')
def printAndLogDefault(text):
    with open('./log/log_main.txt','a') as obj_file:
        time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        writeInfo=time_str+'\t'+text+'\n'
        obj_file.write(writeInfo)
        obj_file.close()
    ptime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    print('['+ptime+']>>>>>>'+text)

# 写入日志(默认'./log/log_main.txt')
def logDefault(text):
    with open('./log/log_main.txt','a') as obj_file:
        time_str = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        writeInfo = time_str +'\t'+text+'\n'
        obj_file.write(writeInfo)
        obj_file.close()

# 获取标准时间字符串
def stdTimeStr():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    
# 打印基本信息
def printBasicInfo(id,name,version,release_time,latest_running_time):
    printInfo="ID:\t\t\t"+id+'\n'+"Name:\t\t\t"+name+'\n'+"Version:\t\t"+version+'\n'+"Release Time:\t\t"+release_time+'\n'+"Latest Running Time:\t"+latest_running_time+'\n'
    print(('='*50+'\n')+('='*50))
    print(printInfo)
    print('='*50)

# 日志基本信息(默认'./log/log_main.txt')
def logBasicInfoDefault(id,name,version,release_time,latest_running_time):
    with open('./log/log_main.txt','a') as obj_file:
        obj_file.write(('='*50+'\n')+('='*50+'\n'))
        writeInfo="ID:\t\t\t"+id+'\n'+"Name:\t\t\t"+name+'\n'+"Version:\t\t\t"+version+'\n'+"Release Time:\t\t"+release_time+'\n'+"Latest Running Time:\t"+latest_running_time+'\n'
        obj_file.write(writeInfo)
        obj_file.write('='*50+'\n')
        obj_file.close()

# 打印提示信息
def printTips():
    print("#"*50)
    print(">>>loading......")
    print(">>>需要安装chrome浏览器，建议使用默认安装位置")

# 检查是否无text按钮
def check(text, browser):
    buttons = browser.find_elements_by_tag_name('button')
    for button in buttons:
        if button.get_attribute("textContent").find(text) >= 0:
            return True
    return False

# 清理日志文件
def clearLog(file):
    with open(file,'w') as obj_file:
        obj_file.truncate()
        obj_file.close()


def getDateStr():
    return time.strftime('%Y-%m-%d',time.localtime())

# 打卡时间过了吗
def isTimeOver():
    ltime = time.localtime(time.time())
    h = ltime.tm_hour
    m = ltime.tm_min
    if h>=15 :
        return True
    else :
        return False

