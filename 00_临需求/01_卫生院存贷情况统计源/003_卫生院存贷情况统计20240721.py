import pandas as pd
import chardet

# 对公存款 20240630
Dpt_20240630 = '/Users/fengliang/Desktop/卫生类账户统计 20240720/卫生类存款20240630.xlsx'
# 对公存款 20231231
Dpt_20231231 = '/Users/fengliang/Desktop/卫生类账户统计 20240720/卫生类存款20240630.xlsx'
# 对公贷款 20240630
Loan_20240630 = '/Users/fengliang/Desktop/卫生类账户统计 20240720/卫生类贷款 20240630.xlsx'
# 禁用科学计数法
pd.set_option('display.float_format', lambda x: '%.f' % x)

df_Dpt_20240630 = pd.read_excel(Dpt_20240630, header=0, dtype={'账户名称': str, '账户性质': str})

df_Dpt_20231231 = pd.read_excel(Dpt_20231231, header=0, dtype={'账户名称': str, '账户性质': str})

df_Loan_20240630 = pd.read_excel(Loan_20240630, header=0, dtype={'账户名称': str, '账户性质': str})

# 对所有字符型列去除两边空格
df_Dpt_20240630 = df_Dpt_20240630.map(lambda x: x.strip() if isinstance(x, str) else x)
df_Dpt_20231231 = df_Dpt_20231231.map(lambda x: x.strip() if isinstance(x, str) else x)
df_Loan_20240630 = df_Loan_20240630.map(lambda x: x.strip() if isinstance(x, str) else x)

# 使用 merge 方法进行左连接
Dpt_merge = df_Dpt_20240630.merge(df_Dpt_20231231, how='left', on=['客户外部账户号'], suffixes=('_0630', '_1231'))

# 连接贷款
Dpt_merge_loan = Dpt_merge.merge(df_Loan_20240630, how='left', on=['客户号_0630'], suffixes=(None, '_贷款_20240630'))
# 筛选出 '客户名称_0630' 字段中包含 '卫生' 或 '医院' 的记录
Dpt_merge_loan_end = Dpt_merge_loan[Dpt_merge_loan['客户名称_0630'].str.contains('卫生|医院')]
# 去除重复的记录
Dpt_merge_loan_end = Dpt_merge_loan_end.drop_duplicates()
# 取消科学计数法
# # 输出excel
Dpt_merge.to_excel('/Users/fengliang/Desktop/卫生类账户统计 20240720/Dpt_merge.xlsx', index=False)
Dpt_merge_loan.to_excel('/Users/fengliang/Desktop/卫生类账户统计 20240720/Dpt_merge_loan.xlsx', index=False)
Dpt_merge_loan_end.to_csv('/Users/fengliang/Desktop/卫生类账户统计 20240720/Dpt_merge_loan_end.csv', index=False)
# 使用 xlsxwriter 引擎保存到 Excel 文件并设置单元格格式
file_path = '/Users/fengliang/Desktop/卫生类账户统计 20240720/Dpt_merge_loan_end.xlsx'
with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
    Dpt_merge_loan_end.to_excel(writer, index=False, sheet_name='Sheet1')

    # 获取 xlsxwriter workbook 和 worksheet 对象
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # 创建数值格式
    format_number = workbook.add_format({'num_format': '0'})

    # 设置单元格格式
    for column in Dpt_merge_loan_end.columns:
        col_idx = Dpt_merge_loan_end.columns.get_loc(column) + 1  # 获取列索引，+1 因为 Excel 是从1开始计数
        worksheet.set_column(col_idx, col_idx, None, format_number)

print(f'DataFrame saved to {file_path} with number format.')
print("合并完成")
