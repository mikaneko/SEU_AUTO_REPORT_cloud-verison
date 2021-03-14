# -*- coding:utf-8 -*-

import socket
import threading
import os
import json

import configtool
import logtool as lt


def threadhandler(c_obj, c_a_p):
    try:
        lt.pl_info('%s:%s CONNECT' % (c_a_p[0], c_a_p[1]), stimestr,
                   is_add_timestamp, is_log_print_info, is_show_print_info)
        while True:
            received_data_str = c_obj.recv(1024).decode()
            lt.pl_info('%s:%s GET = %s' % (
                c_a_p[0], c_a_p[1], received_data_str), stimestr,
                       is_add_timestamp, is_log_print_info, is_show_print_info)

            # IMPORTANT
            if received_data_str == '/exit':
                lt.pl_info('%s:%s EXIT' % (c_a_p[0], c_a_p[1]), stimestr,
                           is_add_timestamp, is_log_print_info, is_show_print_info)
                sending_data_str = 'YOU EXIT'
                c_obj.sendall(sending_data_str.encode())
                c_obj.close()
                return
            if received_data_str.strip() == '/help':
                sending_data_str = '<<<HELP>>>\n' \
                                   'Thanks for using SEU_REPORT_CLOUD_VERSION\n' \
                                   'Here are tips for you\n' \
                                   '/help == show all commands for you\n' \
                                   '/exit == exit the program\n' \
                                   '/op [PASSWORD] == raise your operation level to OP\n' \
                                   '/apply [Name] [username] [password] == apply for auto report\n' \
                                   '/deapply [Name] [username] [password] == apply for removing auto report\n\n' \
                                   '<<<OP HELP>>>\n' \
                                   '/help == show all commands for you\n' \
                                   '/deop == quit the OP level\n' \
                                   '/list == list all user and info' \
                                   '/add [Name] [username] [password] == add a new user\n' \
                                   '/del [uid] == delete a user\n' \
                                   '/exit == exit the program\n'
                c_obj.sendall(sending_data_str.encode())
                continue
            if received_data_str == '/op':
                sending_data_str = 'PLEASE INPUT PASSCODE AFTER COMMAND'
                c_obj.sendall(sending_data_str.encode())
                continue
            if received_data_str.startswith('/apply '):
                with open('./apply.txt', 'a') as file:
                    file.write(received_data_str.split(' ')[1] + ' ' + received_data_str.split(' ')[2] + ' ' +
                               received_data_str.split(' ')[3] + '\n')
                    sending_data_str = 'you have submit an apply'
                    c_obj.sendall(sending_data_str.encode())
                    continue
            if received_data_str.startswith('/deapply '):
                with open('./deapply.txt', 'a') as file:
                    file.write(received_data_str.split(' ')[1] + ' ' + received_data_str.split(' ')[2] + ' ' +
                               received_data_str.split(' ')[3] + '\n')
                    sending_data_str = 'you have submit an apply for remove'
                    c_obj.sendall(sending_data_str.encode())
                    continue
            if received_data_str.startswith('/op '):
                if received_data_str.split(' ')[1].strip() == op_pass:
                    sending_data_str = '[OP]YOU ARE OP NOW'
                    c_obj.sendall(sending_data_str.encode())
                    while True:
                        received_data_str = c_obj.recv(1024).decode()
                        lt.pl_info('%s:%s GET = %s [AS OP]' % (
                            c_a_p[0], c_a_p[1], received_data_str), stimestr,
                                   is_add_timestamp, is_log_print_info, is_show_print_info)
                        if received_data_str.strip() == '/deop':
                            sending_data_str = 'YOU ARE NOT OP ANY MORE'
                            c_obj.sendall(sending_data_str.encode())
                            break
                        if received_data_str.strip() == '/help':
                            sending_data_str = '<<<HELP>>>\n' \
                                               'Thanks for using SEU_REPORT_CLOUD_VERSION\n' \
                                               'Here are tips for you\n' \
                                               '/help == show all commands for you\n' \
                                               '/exit == exit the program\n' \
                                               '/op [PASSWORD] == raise your operation level to OP\n' \
                                               '/apply [Name] [username] [password] == apply for auto report\n' \
                                               '/deapply [Name] [username] [password] == apply for removing auto report\n\n' \
                                               '<<<OP HELP>>>\n' \
                                               '/help == show all commands for you\n' \
                                               '/deop == quit the OP level\n' \
                                               '/list == list all user and info' \
                                               '/add [Name] [username] [password] == add a new user\n' \
                                               '/del [uid] == delete a user\n' \
                                               '/exit == exit the program\n'
                            c_obj.sendall(sending_data_str.encode())
                            continue
                        if received_data_str.strip() == '/list':
                            with open('../daka/encdata/userlist.json', 'r') as file:
                                tmp_str = str(file.readline())
                                file.close()
                                tmp_list = json.loads(tmp_str.strip())
                                tmp_format = json.dumps(tmp_list, indent=4)
                            sending_data_str = tmp_format
                            c_obj.sendall(sending_data_str.encode())
                            continue
                        if received_data_str.startswith('/add '):
                            var_1 = received_data_str.split(' ')[1].strip()
                            var_2 = received_data_str.split(' ')[2].strip()
                            var_3 = received_data_str.split(' ')[3].strip()
                            with open('../daka/encdata/userlist.json', 'r') as file:
                                filecontent = file.readline()
                                now_list = json.loads(filecontent)
                                uid = int(len(now_list) + 1)
                                name = var_1
                                username = var_2
                                password = var_3
                                new_dict = {'uid': uid,
                                            'name': name,
                                            'username': username,
                                            'password': password}
                                now_list.append(new_dict)
                                new_list_format = json.dumps(now_list)
                                file.close()
                            with open('../daka/encdata/userlist.json', 'w') as file:
                                file.write(new_list_format)
                                file.close()
                            sending_data_str = '[OP]a user has been appended'
                            c_obj.sendall(sending_data_str.encode())
                            continue
                        if received_data_str.startswith('/del '):
                            delete_uid = int(received_data_str.split(' ')[1].strip())
                            with open('../daka/encdata/userlist.json', 'r') as file:
                                filecontent = file.readline()
                                now_list = json.loads(filecontent)
                                now_list.pop(delete_uid - 1)
                                while delete_uid - 1 < len(now_list):
                                    now_list[delete_uid - 1]['uid'] -= 1
                                    delete_uid += 1
                                new_list_format = json.dumps(now_list)
                                file.close()
                            with open('../daka/encdata/userlist.json', 'w') as file:
                                file.write(new_list_format)
                                file.close()
                            sending_data_str = '[OP]a user has been removed'
                            c_obj.sendall(sending_data_str.encode())
                            continue
                        if received_data_str.strip() == '/exit':
                            sending_data_str = 'YOU ARE NOT OP AND YOU EXIT'
                            c_obj.sendall(sending_data_str.encode())
                            c_obj.close()
                            return
                        sending_data_str = '[OP]WRONG COMMAND'
                        c_obj.sendall(sending_data_str.encode())
                    continue
                else:
                    sending_data_str = 'YOU CANNOT BE OP BECAUSE WRONG PASSCODE'
                    c_obj.sendall(sending_data_str.encode())
                    continue
            sending_data_str = 'WRONG COMMAND'
            c_obj.sendall(sending_data_str.encode())

    except Exception as e:
        lt.pl_warning('%s:%s CONNECT ERROR(201):' % (
            c_a_p[0], c_a_p[1]), stimestr, is_add_timestamp, is_log_print_info, is_show_print_info)
        print(e)


def deal_method_1(c_obj, c_a_p):
    threadhandler(c_obj, c_a_p)


if __name__ == '__main__':
    # 启动时间戳
    stimestr = lt.gettimestr()
    # 创建各种目录
    if not os.path.exists('./config'):
        os.mkdir('./config')
    if not os.path.exists('./log'):
        os.mkdir('./log')

    config_console_dict = configtool.config_console()
    if config_console_dict['is_show_print_info'].lower() == 'true':
        is_show_print_info = True
    else:
        is_show_print_info = False
    if config_console_dict['is_log_print_info'].lower() == 'true':
        is_log_print_info = True
    else:
        is_log_print_info = False
    if config_console_dict['is_add_timestamp'].lower() == 'true':
        is_add_timestamp = True
    else:
        is_add_timestamp = False

    config_link_dict = configtool.config_link()
    address = config_link_dict['address']
    port = config_link_dict['port']
    su_pass = config_link_dict['su_pass']
    op_pass = config_link_dict['op_pass']

    # 读取各种目录

    s_add_port = (address, int(port))

    # ipv4 tcp
    sk_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk_obj.bind(s_add_port)
    sk_obj.listen(5)
    lt.pl_system('SERVER STARTED', stimestr, is_add_timestamp, is_log_print_info, is_show_print_info)

    while True:
        connect_obj, c_add_port = sk_obj.accept()
        new_thread = threading.Thread(target=deal_method_1, args=(connect_obj, c_add_port))
        new_thread.start()
