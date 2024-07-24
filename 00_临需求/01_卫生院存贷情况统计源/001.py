import numpy as np
import openpyxl
import os
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime
from prettytable import prettytable
from tabulate import tabulate


def delete_files_not_today(start_name):
    # 获取当前日期
    current_date = datetime.now().strftime('%Y%m%d')
    # 获取当前目录
    current_directory = os.getcwd()
    # 遍历当前目录下的所有文件
    for file_name in os.listdir(current_directory):
        # 检查是否是文件，并且文件名以 '惠商户差异化进度表_' 开头
        if os.path.isfile(file_name) and file_name.startswith(start_name):
            # 获取文件名和扩展名
            name, ext = os.path.splitext(file_name)
            # 检查文件是否以今天的日期结尾且扩展名为 .xlsx
            if not name.endswith(current_date) or ext != '.xlsx':
                # 删除文件
                os.remove(file_name)
                print(f"文件 {file_name} 已成功删除")


# 获取当前日期
current_date = datetime.now().strftime('%Y%m%d')
# 源数据地址
file_path_1 = './商户分户统计表_20240625.xlsx'
# 输出数据地址
file_path_2 = './惠商户差异化进度表_' + current_date + '.xlsx'
# 输出数据地址
file_path_3 = './惠商户差异化进度表out_' + current_date + '.xlsx'

df_excel = pd.read_excel(file_path_1, engine='openpyxl')
df_excel['资金留存率'] = df_excel['结算账户年日均存款余额'] / df_excel['本年交易金额']

# 对所有字符型列去除两边空格
df = df_excel.map(lambda x: x.strip() if isinstance(x, str) else x)
df_excel
# 选择特定的字段
selected_columns = ['商户名称', '本年交易金额', '本年交易月数', '本年手续费支出', '本年手续费收入',
                    '结算账户年日均存款余额', '资金留存率']
df_selected = df[selected_columns]


# 计算 本年交易金额 除以 本年交易月数，判断是否月均大于 1 万元
def calculate_flag(row):
    # 检查分母是否为零
    if row['本年交易月数'] == 0:
        return 0
    elif row['本年交易金额'] / row['本年交易月数'] >= 10000:
        return 1
    else:
        return 0


# 复制副本
df_selected = df_selected.copy()
# 应用函数_月均条件
df_selected.loc[:, '月均大于一万标识'] = df_selected.apply(calculate_flag, axis=1)


# 计算 资金留存率区间范围
def calculate_range(row):
    if row['资金留存率'] >= 0.4:
        return 1
    elif 0.3 <= row['资金留存率'] < 0.4:
        return 2
    elif 0.2 <= row['资金留存率'] < 0.3:
        return 3
    elif 0.1 <= row['资金留存率'] < 0.2:
        return 4
    elif row['资金留存率'] < 0.1:
        return 5


# 计算 手续费支出前 20% 的商户
# 计算前 20% 的数量
top_20_count = int(len(df_selected) * 0.2)
# 对数据框按手续费支出排序
df_selected = df_selected.sort_values(by='本年手续费支出', ascending=False)
# 标记前 20% 的记录
df_selected['是否前20%'] = 0
df_selected.iloc[:top_20_count, df_selected.columns.get_loc('是否前20%')] = 1
# 应用函数_留存率区间
df_selected.loc[:, '资金留存率区间'] = df_selected.apply(calculate_range, axis=1)
# 创建结果输出DataFrame
import pandas as pd

# 定义列字段
columns = ['留存率', '月均交易额度大于1万元商户数', '累计交易额', '计费交易额', '补贴手续费', '实收手续费', '执行扣率',
           '扣率', '月均交易额度大于1万元商户数', '累计交易额', '模拟应扣费(单位：万元)', '目前扣费户数',
           '实际收费数(单位：万元)']
# 定义行数据
data = [
    ['留存率0.4及以上', 51548, 161.20, 0.00, 0.40, 0.00, '完全免费', 0.0000, None, None, None, None, None],
    ['留存率[0.3-0.4)', 17699, 66.28, 45.04, 0.12, 0.05, '执行4折0.1%', 0.0010, None, None, None, None, None],
    ['留存率[0.2-0.3)', 31869, 128.84, 90.60, 0.19, 0.14, '执行6折0.15%', 0.0015, None, None, None, None, None],
    ['留存率[0.1-0.2)', 73863, 343.07, 254.43, 0.35, 0.51, '执行8折0.2%', 0.0020, None, None, None, None, None],
    ['留存率低于0.1', 463206, 3506.74, 2950.89, 1.39, 7.38, '执行基准扣率0.25%', 0.0025, None, None, None, None, None],
    ['总计/平均', None, None, None, None, None, None, None, None, None, None, None, None]
]
# 创建 DataFrame
df_out = pd.DataFrame(data, columns=columns)

# 开始计算
# 分组bys姓名
# 筛选出月均大于一万的记录
filtered_df = df_selected[df_selected['月均大于一万标识'] == 1]
# 根据资料留存率区间统计商户数
cnt_rate = filtered_df.groupby('资金留存率区间').size().reset_index(name='总记录数')
print(cnt_rate)
# 01_创建一个 ExcelWriter 对象使用 xlsxwriter 作为引擎
with pd.ExcelWriter(file_path_2, engine='xlsxwriter') as writer1, pd.ExcelWriter(file_path_3,
                                                                                 engine='xlsxwriter') as writer2:
    # 获取 workbook 和 worksheet 对象
    workbook1 = writer1.book
    workbook2 = writer2.book
    # 创建居中对齐格式
    center_format = workbook1.add_format({'align': 'center', 'valign': 'vcenter'})
    # 写入数据并应用格式到第一个文件
    df_selected.to_excel(writer1, sheet_name='Sheet1', index=False)
    worksheet1 = writer1.sheets['Sheet1']
    for col_num, col_name in enumerate(df_selected.columns):
        column_width = len(col_name) + 2
        worksheet1.set_column(col_num, col_num, column_width, center_format)
    # 写入数据并应用格式到第二个文件
    df_out.to_excel(writer2, sheet_name='Sheet1', index=False)
    worksheet2 = writer2.sheets['Sheet1']
    for col_num, col_name in enumerate(df_out.columns):
        column_width = len(col_name) + 2
        #     print(column_width)
        worksheet1.set_column(col_num, col_num, column_width, center_format)



# 删除旧文件
delete_files_not_today('惠商户差异化进度表_')
delete_files_not_today('惠商户差异化进度表out_')
print("Excel 文件已生成设置居中对齐和自适应列宽,并保存")
