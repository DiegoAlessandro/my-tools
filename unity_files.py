# coding: utf-8
import codecs
import csv
import sys
import xlrd
import os
import datetime


def get_list_2d_all(sheet):
    return [sheet.row_values(row) for row in range(sheet.nrows)]


def deduplication(target_list=[]):
    dst = list(set(target_list))
    if dst[0] == '':
        dst = dst[1:]
    dst = list(map(int, dst))
    print('重複削除後のデータ数:{:,}件'.format(len(dst)))
    return dst


def collect_files(dir_path):
    spice_id_list = []
    files = os.listdir(dir_path)
    files_file = [f for f in files if os.path.isfile(os.path.join(dir_path, f)) and f != '.DS_Store']
    print('--{} files found!'.format(len(files_file)))
    [print('{}.{}'.format(i + 1, f)) for i, f in enumerate(files_file)]
    for file_name in files_file:
        file_path = '{}/{}'.format(dir_path, file_name)
        print('processing... {}'.format(file_path))
        with codecs.open(file_path, "r", "Shift-JIS", "ignore") as f:
            reader = csv.reader(f)
            l = [row for row in reader]
            try:
                col_num = l[0].index('spice id')
                tmp_l = [x[col_num] for x in l[1:]]
                spice_id_list = spice_id_list + tmp_l

            except ValueError as e:
                print(e)

    print('Total spice id is {:,}.'.format(len(spice_id_list)))
    return spice_id_list


if __name__ == '__main__':

    print('ダウンロードしたCSVファイルが格納されているフォルダーのフルパスを入力してください。')
    dir_path = input()

    spice_id_list = []
    spice_id_list = collect_files(dir_path)

    spice_id_list = deduplication(spice_id_list)

    out_file_name = '重複削除_{}'.format("{0:%Y%m%d%H%M%S}".format(datetime.datetime.now()))
    out_file_path = '{}/{}/{}.csv'.format('/'.join(dir_path.split('/')[:-1]), 'out', out_file_name)
    with open(out_file_path, 'w') as f:
        writer = csv.writer(f, lineterminator='\n')  # 改行コード（\n）を指定しておく
        for i in spice_id_list:
            writer.writerow([str(i)])
