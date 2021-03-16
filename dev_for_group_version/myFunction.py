import time
import json

# 读取配置
def get_config_main():
    try:
        with open('./config/config_main.json', 'r') as file:
            return_str = file.readline()
            file.close()
            print('>>config loaded')
    except:
        print('>>config loaded error')
        print('>>guiding you to complete')
        time.sleep(2)
        with open('./config/config_main.json', 'w') as file:
            chrome_link = input('>>>INPUT: chromedriver link:  ')
            web_link = input('>>>INPUT: web link:  ')
            temperature = input('>>>INPUT: std temperature:  ')
            tmp_dict = {"chrome_driver_link": chrome_link,
                        "web_link": web_link,
                        "temperature": temperature}
            return_str = json.dumps(tmp_dict) + '\n'
            file.write(return_str)
            file.close()
    return return_str

# 用户管理操作(2)
def manage_userlist_main():
    while True:
        print('-'*50)
        print('>>>user manage operation')
        print('   (1)list all users and information')
        print('   (2)append a new user')
        print('   (3)delete a user')
        print('   (0)QUIT user manage')
        operation = input('>>>INPUT： operation code:  ')
        if operation == '1':
            with open('./encdata/userlist.json', 'r') as file:
                tmp_str = str(file.readline())
                file.close()
                tmp_list = json.loads(tmp_str.strip())
                tmp_format = json.dumps(tmp_list, indent=4)
                print(tmp_format)
        elif operation == '2':
            with open('./encdata/userlist.json', 'r') as file:
                filecontent = file.readline()
                now_list = json.loads(filecontent)
                uid = int(len(now_list) + 1)
                name = input('>>>INPUT: name:  ')
                usernum = input('>>>INPUT: usernum:  ')
                password = input('>>>INPUT: password:  ')
                new_dict = {'uid': uid,
                            'name': name,
                            'usernum': usernum,
                            'password': password}

                now_list.append(new_dict)
                new_list_format = json.dumps(now_list)
                file.close()
            with open('./encdata/userlist.json', 'w') as file:
                file.write(new_list_format)
                file.close()
            print('>>>a new user has been appended')
        elif operation == '3':
            delete_uid = int(input('>>>INPUT: the uid of user to be deleted:  '))
            with open('./encdata/userlist.json', 'r') as file:
                filecontent = file.readline()
                now_list = json.loads(filecontent)
                now_list.pop(delete_uid-1)
                while delete_uid-1 < len(now_list):
                    now_list[delete_uid-1]['uid'] -= 1
                    delete_uid += 1
                new_list_format = json.dumps(now_list)
                file.close()
            with open('./encdata/userlist.json', 'w') as file:
                file.write(new_list_format)
                file.close()
            print('>>>a user has been deleted')
        elif operation == '0':
            print('>>>you have quit user manage')
            break
        else:
            print('>>>wrong operation, try again')
            continue

# 每日健康打卡记录(3)
def print_user_log():
    pass # todo

