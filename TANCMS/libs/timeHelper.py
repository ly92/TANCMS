import time
import re

def formatTime(time_str):
    s = strToTimeStamp(time_str)
    timeArray = time.localtime(s)
    date = time.strftime("%Y-%m-%dT%H:%M:%S.%j%z", timeArray)
    return date


def strToTimeStamp(time_str):
    if type(time_str) == str:
        time_str = time_str.strip()
    elif type(time_str) == int or type(time_str) == float:
        if int(time_str) > 1000000000:
            return int(time_str)
        else:
            return int(time.time())
    time_int = re.findall('\d+', time_str, re.S)
    if len(time_int) == 1:
        if int(time_str) > 1000000000:
            return int(time_str)
        else:
            return int(time.time())

    if time_str == '刚刚':
        return int(time.time())
    if time_str.endswith('分钟前'):
        num = int(time_str.replace('分钟前', '').strip())
        return int(time.time()) - num * 60
    if time_str.endswith('小时前'):
        num = int(time_str.replace('小时前', '').strip())
        return int(time.time()) - num * 60 * 60
    if time_str.endswith('天前'):
        num = int(time_str.replace('天前', '').strip())
        return int(time.time()) - num * 60 * 60 * 24
    if '年' in time_str and '月' in time_str and '日' in time_str:
        time_s = time_str.split(':')
        format_str = ''
        if len(time_s) == 3:
            format_str = '%Y年%m月%d日 %H:%M:%S'
        elif len(time_s) == 2:
            format_str = '%Y年%m月%d日 %H:%M'
        elif len(time_s) == 1:
            if len(time_str.split(' ')) == 2:
                format_str = '%Y年%m月%d日 %H'
            else:
                format_str = '%Y年%m月%d日'
        time_array = time.strptime(time_str, format_str)
        return int(time.mktime(time_array))
    if '-' in time_str:
        time_s = time_str.split(':')
        format_str = ''
        if len(time_s) == 3:
            format_str = '%Y-%m-%d %H:%M:%S'
        elif len(time_s) == 2:
            format_str = '%Y-%m-%d %H:%M'
        elif len(time_s) == 1:
            if len(time_str.split(' ')) == 2:
                format_str = '%Y-%m-%d %H'
            else:
                format_str = '%Y-%m-%d'
        time_array = time.strptime(time_str, format_str)
        return int(time.mktime(time_array))

    try:
        format_str = '%a %b %d %H:%M:%S %z %Y'
        time_array = time.strptime(time_str, format_str)
        t = int(time.mktime(time_array))
    except:
        pass
    finally:
        if t > 0:
            return t

    return int(time.time())


if __name__ == '__main__':
    # s = '2020-11-02'
    # s = '123123123'
    # s = 1231231231
    s = 1605062386.83242
    print(type(s))
    date = formatTime(s)
    print(date)
