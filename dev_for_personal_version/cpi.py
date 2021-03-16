def printBasicInfo(id,name,version,release_time,latest_running_time):
    printInfo="ID:\t\t\t"+id+'\n'+"Name:\t\t\t"+name+'\n'+"Version:\t\t"+version+'\n'+"Release Time:\t\t"+release_time+'\n'+"Latest Running Time:\t"+latest_running_time+'\n'
    print(printInfo)

def versionUpdateInfo():
    print('-'*50)
    # 0.1.1
    print('>>0.1.1内容：')
    print('>>实现基本的个人打卡功能')
    print('-'*50)
    # 0.2.1
    print('>>0.2.1版本更新内容:')
    print('>>1. 由"计时器打卡"转变为"定时检查时间打卡"')
    print('>>2. 优化代码和程序逻辑')
    print('>>3. 优化输出和日志显示方式')
    print('>>4. 优化发布版文件结构，.exe单文件更加清晰')
    print('-'*50)
    # 0.2.2
    print('>>0.2.2版本更新内容:')
    print('>>1. 修复部分bug')
    print('>>提示  ： 如果遇到不能打卡的情况，请删除userdata文件夹')
    print('>>提示  ： userdata文件夹下明文存储着账号和密码，注意安全')
    print('>>提示  ： log文件夹下存储着日志文件，不会存储个人信息')
    print('>>标注由： atarashichiaki@hotmail.com')
    print('-'*50)

