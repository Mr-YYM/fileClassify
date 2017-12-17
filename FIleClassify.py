# -*- coding: utf-8 -*
"""
需求如下：
一、把程序所在目录下的所有文件, 按照他们的日期创建文件夹, 然后把该日期文件剪切到该文件夹, 完成按日期文件夹分类。

具体说明：
1、例如：创建2017-08-11 这种格式的目录, 里面就存放这个日期的文件
2、文件的日期  以文件的创建时间/修改时间/访问时间中  三者的最旧的那个时间为准来创建文件夹
3. 文件夹的格式是2017-08-11

二、上述的反转，将文件从文件夹中取出

具体说明：
1、文件取出后，将空的文件夹删除

"""

import os
import shutil
import time
import re


def get_file_info(date_format):
    date_info = {}
    num_info = {}
    for each_file in os.listdir():
        if os.path.isfile(each_file) and each_file != os.path.basename(__file__):
            m_time = time.localtime(os.stat(each_file).st_mtime)  # 修改时间
            a_time = time.localtime(os.stat(each_file).st_atime)  # 访问时间
            c_time = time.localtime(os.stat(each_file).st_ctime)  # 创建时间
            min_time = min(m_time, a_time, c_time)
            date_info[each_file] = time.strftime(date_format, min_time)

    for item in sort_a_date_list(set(date_info.values()), date_format):  # 对日期进行排序并统计数量
        num_info[item] = list(date_info.values()).count(item)
    return date_info, num_info


def insert_sort(lists):
    # 插入排序
    count = len(lists)
    for i in range(1, count):
        key = lists[i]
        j = i - 1
        while j >= 0:
            if lists[j] > key:
                lists[j + 1] = lists[j]
                lists[j] = key
            j -= 1
    return lists


def sort_a_date_list(date_arr, date_format):
    date_arr_in_int = [time.mktime(time.strptime(i, date_format)) for i in date_arr]  # 将日期转换为int后排序
    return [time.strftime(date_format, time.localtime(i))
            for i in insert_sort(date_arr_in_int)]  # 将int日期格式化


def show_num_info(num_info):
    for k, v in num_info.items():
        print("%s有%d个" % (k, v))


def classify(date_format):
    old_date = ''
    date_info, num_info = get_file_info(date_format)
    a=1
    # dates = date_info.values()
    # for file, date in date_info.items():
    #     if file == os.path.basename(__file__) or os.path.isdir(file):
    #         continue
    #     elif os.path.splitext(file)[1] != '.md':
    #         if date not in os.listdir():
    #             os.mkdir(date)
    #         shutil.move(file, os.path.join(date, file))
    for each_file in os.listdir():
        if each_file == os.path.basename(__file__) or os.path.isdir(each_file):  # 跳过程序本身与文件夹
            continue
        elif os.path.splitext(each_file)[1] != '.md':
            date = date_info[each_file]
            if date not in os.listdir():  # 建立相关文件夹
                os.mkdir(date)
            if old_date != date:
                print("正在处理%s,文件总数：%d" % (date, num_info[date]))
            old_date = date
            try:
                shutil.move(each_file, os.path.join(date, each_file))  # 移动文件
            except:
                continue


def reverse_action():
    for each_dir in os.listdir():
        if os.path.isdir(each_dir) and re.match('\.', each_dir) is None:
            print("正在处理文件夹%s，文件个数为%d" % (each_dir, len(os.listdir(each_dir))))
            for each_file in os.listdir(each_dir):
                shutil.move(os.path.join(each_dir, each_file), each_file)
            try:
                os.removedirs(each_dir)
            except:
                continue


def main():
    response = input("请选择一个进行操作：\n1、按日期将文件分类\n2、将程序目录的文件夹里所有文件取出\n")
    if response == '1':
        do_classify()
    elif response == '2':
        start = time.time()
        reverse_action()
        end = time.time()
        print("运行时间为：%.2f秒" % (end - start))
    else:
        print("等下再来")


def do_classify():
    while 1:
        try:
            format_list = ["%Y", "%Y-%m", "%Y-%m-%d"]
            response = input("请选择分类格式：\n1、按年\n2、按年-月\n3、按年-月-日\n")
            date_format = format_list[int(response) - 1]
            break
        except (IndexError, TypeError, ValueError):
            print("输入错误,请正确输入")
            time.sleep(1)
    date_info = get_file_info(date_format)[1]
    if len(date_info) == 0:
        print("没有可以处理的文件")
    else:
        show_num_info(date_info)
        response = input("汇总信息如上，确定开始操作吗（y/n）\n")
        if response == "y":
            start = time.time()
            classify(date_format)
            end = time.time()
            print("运行时间为：%.2f秒" % (end - start))
        else:
            print("等下再来")


if __name__ == '__main__':
    main()
