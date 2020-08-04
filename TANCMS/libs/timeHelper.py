import time


def strToTimeStamp(time_str):
    time_str = time_str.strip()
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
