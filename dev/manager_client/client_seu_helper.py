# -*- coding:utf-8 -*-

import socket
import os

def load_config():
    config_return = {}
    try:
        with open('./config/client.cfg', 'r') as file:
            line_list = file.readlines()
            for line in line_list:
                if line.startswith('#') or line == '\n':
                    continue
                key = line.split('=*=')[0].strip()
                value = line.split('=*=')[1].strip()
                config_return[key] = value
        return config_return
    except FileNotFoundError:
        print('[WARNING] CANNOT LOAD CONFIG')
        with open('./config/client.cfg', 'w') as file:
            file.write('#THIS FILE IS TO CONFIG SEU_DAILY_REPORT_CLIENT\n'
                       '#ONLY AVAILABLE TO VERSION C_1\n'
                       '#PLEASE FILL ALL CONFIG IN CASE THAT PROGRAM MIGHT RUN IMPROPERLY\n'
                       '#COPYRIGHT CHIAKI AT SOUTHEAST UNIVERSITY, CHINA\n'
                       '\n'
                       '#Report Address\n'
                       'link_address =*= localhost\n'
                       '\n'
                       '#Webdriver Address\n'
                       'link_port =*= 26001\n'
                       '\n'
                       '#END OF CONFIG\n')
        print('[WARNING] WE HELPED YOU CREATE A NEW CONFIG')
        try:
            with open('./config/client.cfg', 'r') as file:
                line_list = file.readlines()
                for line in line_list:
                    if line.startswith('#') or line == '\n':
                        continue
                    key = line.split('=*=')[0].strip()
                    value = line.split('=*=')[1].strip()
                    config_return[key] = value
            return config_return
        except Exception as e:
            print('[ERROR] UNKNOWN ERROR(101): ' + str(e))
    except Exception as e:
        print('[ERROR] UNKNOWN ERROR(102): ' + str(e))


if __name__ == '__main__':
    if not os.path.exists("config"):
        os.mkdir("config")
    # 读取设置
    config_dict = load_config()
    link_address = config_dict['link_address']
    link_port = int(config_dict['link_port'])
    print('SEU AUTO REPORT CLOUD VERSION\n'
          'Type "/help" to get hint.')

    try:
        server_add_port = (link_address, link_port)
        sk_obj = socket.socket()
        sk_obj.connect(server_add_port)

        while True:

            sending_data_str = input('输入内容：').strip()
            if sending_data_str == '':
                continue
            sk_obj.sendall(sending_data_str.encode())

            if sending_data_str == '/exit':
                print('客户端退出')
                break

            received_data_str = sk_obj.recv(1024).decode()

            print('Received: %s' % received_data_str)

        sk_obj.close()

    except Exception as e:
        print('连接错误')
