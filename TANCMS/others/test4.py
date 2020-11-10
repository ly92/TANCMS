import xlrd
import xlwt
import os

src = '/Users/ly/Desktop/excel/'


def file_name(file_dir):
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('My Worksheet')
    new_i = 1
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            filePath = src + file

            x1 = xlrd.open_workbook(filePath)

            sheet1 = x1.sheet_by_name("new sheet")
            rows = sheet1.nrows
            clos = sheet1.ncols

            for i in range(1, rows):
                labels = sheet1.row_values(i, 0, clos)
                for j in range(clos):
                    # 写入excel
                    # 参数对应 行, 列, 值
                    worksheet.write(new_i, j, labels[j])
                new_i += 1

    workbook.save('Excel_test.xls')


if __name__ == '__main__':
    file_name(src)