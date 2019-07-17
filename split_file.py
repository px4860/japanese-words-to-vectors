# -*- coding:utf-8 -*-
from datetime import datetime


def Main(flag_s, source, target):
    source_dir = source
    target_dir = target

    # 计数器
    flag = 0

    # 文件名
    name = 1

    # 存放数据
    dataList = []

    print("开始。。。。。")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    with open(source_dir, 'r', encoding='utf-8') as f_source:
        for line in f_source:
            flag += 1
            dataList.append(line)
            if flag == flag_s:
                with open(target_dir + "ja_token_list_" + str(name) + ".txt", 'w+', encoding='utf-8') as f_target:
                    for data in dataList:
                        f_target.write(data)
                name += 1
                flag = 0
                dataList = []

    # 处理最后一批数据
    with open(target_dir + "ja_token_list_" + str(name) + ".txt", 'w+', encoding='utf-8') as f_target:
        for data in dataList:
            f_target.write(data)

    print("完成。。。。。")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    # 先设定一下分行的行数，以及输入文件和输出地址
    # 以下是示例
    # split请先在项目内创建split目录
    Main(500, 'jawiki-latest-text-tokens.txt', 'split/')