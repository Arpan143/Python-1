#!usr/bin/python
# coding=utf-8

import xlrd


def main():
    workbook = xlrd.open_workbook('E:\\1.xlsx')
    sheet = workbook.sheet_by_name('1')  # sheet = workbook.sheet_by_index(0) 等价于 workbook.sheets()[0]
    namelist = sheet.col_values(0)[1:]  # sheet.row_values(i) 行的数值
    print namelist
    print sheet.nrows  # print sheet.ncols
    print sheet.cell(0, 0).values  # 单元格
    # sheet.put_cell(row, col, ctype, value, xf)  # type:0 empty,1 string,2 number,3 date,4 boolean,5 error; xf = 0格式化


if __name__ == '__main__':
    print '''
 _        _   _      _  _    __    _  __________  _           _
| |      | | \ \    / /| |  /  \  | ||  ________|| |         | |
| |______| |  \ \  / / | | / /\ \ | || |________ | |         | |
|  ______  |   \ \/ /  | | | || | | ||  ________|| |         | |
| |      | |    \  /   | |_| || |_| || |         | |         | |
| |      | |    |  |    \   /  \   / | |________ | |________ | |________
|_|      |_|    |__|     \_/    \_/  |__________||__________||__________|
'''
    main()
