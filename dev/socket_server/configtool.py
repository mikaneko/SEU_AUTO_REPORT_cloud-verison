# -*- coding:utf-8 -*-


def config_console():
    config_return = {}
    try:
        with open('./config/console.cfg', 'r') as file:
            line_list = file.readlines()
            for line in line_list:
                if line.startswith('#') or line == '\n':
                    continue
                key = line.split('=')[0].strip()
                value = line.split('=')[1].strip()
                config_return[key] = value
        return config_return
    except FileNotFoundError:
        print('[WARNING] CANNOT LOAD CONFIG CONSOLE')
        with open('./config/console.cfg', 'w') as file:
            file.write('#THIS FILE IS TO CONFIG THE CONSOLE OF PROGRAM FOR SERVER\n'
                       '#ONLY AVAILABLE TO VERSION S_0.1.1\n'
                       '#PLEASE FILL ALL CONFIG IN CASE THAT PROGRAM MIGHT RUN IMPROPERLY\n'
                       '#COPYRIGHT CHIAKI AT SOUTHEAST UNIVERSITY, CHINA\n'
                       '\n'
                       '#Whether show print information (True,False) (True is default btw)\n'
                       'is_show_print_info = True\n'
                       '\n'
                       '#Whether log print information (True,False) (True is default btw)\n'
                       'is_log_print_info = True\n'
                       '\n'
                       '#Whether add timestamp to show and log (True,False) (True is default btw)\n'
                       'is_add_timestamp = True\n'
                       '\n'
                       '#END OF CONSOLE CONFIG\n')
        print('[WARNING] WE HELPED YOU CREATE A NEW CONFIG CONSOLE')
        try:
            with open('./config/console.cfg', 'r') as file:
                line_list = file.readlines()
                for line in line_list:
                    if line.startswith('#') or line == '\n':
                        continue
                    key = line.split('=')[0].strip()
                    value = line.split('=')[1].strip()
                    config_return[key] = value
            return config_return
        except Exception as e:
            print('[WARNING] UNKNOWN ERROR(101): ' + str(e))
    except Exception as e:
        print('[WARNING] UNKNOWN ERROR(102): ' + str(e))


def config_link():
    config_return = {}
    try:
        with open('./config/link.cfg', 'r') as file:
            line_list = file.readlines()
            for line in line_list:
                if line.startswith('#') or line == '\n':
                    continue
                key = line.split('=')[0].strip()
                value = line.split('=')[1].strip()
                config_return[key] = value
        return config_return
    except FileNotFoundError:
        print('[WARNING] CANNOT LOAD CONFIG LINK')
        with open('./config/link.cfg', 'w') as file:
            file.write('#THIS FILE IS TO CONFIG THE LINK OF PROGRAM FOR SERVER\n'
                       '#ONLY AVAILABLE TO VERSION S_0.1.1\n'
                       '#PLEASE FILL ALL CONFIG IN CASE THAT PROGRAM MIGHT RUN IMPROPERLY\n'
                       '#COPYRIGHT CHIAKI AT SOUTHEAST UNIVERSITY, CHINA\n'
                       '\n'
                       '#Target Address (std IPv4 address)\n'
                       'address = localhost\n'
                       '\n'
                       '#Target Port (26001 is default btw)\n'
                       'port = 26001\n'
                       '\n'
                       '#Super Admin Passcode\n'
                       'su_pass = 123456\n'
                       '\n'
                       '#Op Passcode\n'
                       'op_pass = 123456\n'
                       '\n'
                       '#END OF LINK CONFIG\n')
        print('[WARNING] WE HELPED YOU CREATE A NEW CONFIG LINK')
        try:
            with open('./config/link.cfg', 'r') as file:
                line_list = file.readlines()
                for line in line_list:
                    if line.startswith('#') or line == '\n':
                        continue
                    key = line.split('=')[0].strip()
                    value = line.split('=')[1].strip()
                    config_return[key] = value
            return config_return
        except Exception as e:
            print('[WARNING] UNKNOWN ERROR(101): ' + str(e))
    except Exception as e:
        print('[WARNING] UNKNOWN ERROR(102): ' + str(e))


# test code
if __name__ == '__main__':
    print(config_console())
    print(config_link())
