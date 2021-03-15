# -*- coding:utf-8 -*-
import time


# 以下为基本
def pl_info(text, stimestr, is_timestamp, is_log, is_print):
    time_str = '<' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '> '
    if is_timestamp:
        prefix = '[INFO] ' + time_str
    else:
        prefix = '[INFO] '
    if is_print:
        print(prefix + text)
    if is_log:
        with open('./log/log_' + stimestr, 'a') as file:
            file.write(prefix + text + '\n')


def pl_warning(text, stimestr, is_timestamp, is_log, is_print):
    time_str = '<' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '> '
    if is_timestamp:
        prefix = '[WARNING] ' + time_str
    else:
        prefix = '[WARNING] '
    if is_print:
        print(prefix + text)
    if is_log:
        with open('./log/log_' + stimestr, 'a') as file:
            file.write(prefix + text + '\n')


def pl_system(text, stimestr, is_timestamp, is_log, is_print):
    time_str = '<' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + '> '
    if is_timestamp:
        prefix = '[SYSTEM] ' + time_str
    else:
        prefix = '[SYSTEM] '
    if is_print:
        print(prefix + text)
    if is_log:
        with open('./log/log_' + stimestr, 'a') as file:
            file.write(prefix + text + '\n')


def gettimestr():
    return time.strftime('%Y%m%d%H%M%S', time.localtime())
