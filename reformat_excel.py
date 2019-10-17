# coding: utf-8
import csv
import sys
import xlrd

def get_list_2d_all(sheet):
    return [sheet.row_values(row) for row in range(sheet.nrows)]

if __name__ == '__main__':

    print('手作りのExcelファイルのフルパスを入力してください。>>')
    file_path = input().strip()

    wb = xlrd.open_workbook(file_path)
    sheet = wb.sheet_by_name(wb.sheet_names()[0])
    col = sheet.col(1)
    res = get_list_2d_all(sheet)

    var = []
    for i in res:
        var = var + i

    dst = list(set(var))
    if dst[0] == '':
        dst = dst[1:]
    dst = list(map(int,dst))
    print('重複削除後のデータ数:{:,}件'.format(len(dst)))

    out_file_name = './重複削除_{}'.format(file_path.split('/')[-1].replace('.xlsx','.csv'))
    with open(out_file_name, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')  # 改行コード（\n）を指定しておく
        for i in dst:
            writer.writerow([str(i)])