import pandas as pd

# 应换签商户号
file_path_task = '/Users/fengliang/Documents/Pandas_stns/01_惠商户/01_惠商户分类分级记差异化费率化试点/02_进度核对/应换签商户商户号_基.xlsx'
file_path_0720 = '/Users/fengliang/Documents/Pandas_stns/01_惠商户/01_惠商户分类分级记差异化费率化试点/02_进度核对/商户分户统计表_基表_20240720.csv'
file_path_0728 = '/Users/fengliang/Documents/Pandas_stns/01_惠商户/01_惠商户分类分级记差异化费率化试点/02_进度核对/商户分户统计表_对比_20240728.csv'

try:
    df_file_path_task = pd.read_excel(file_path_task)
    df_file_path_0720 = pd.read_csv(file_path_0720, encoding='gbk')
    df_file_path_0728 = pd.read_csv(file_path_0728, encoding='gbk')
except Exception as e:
    print(e)
print(df_file_path_0720.columns)
usercolumns_merchant_0720 = ['商户编号', '机构号', '机构名称', '商户名称', '商户简称', '本年交易金额', '商户状态',
                             '本年手续费收入', '本年手续费支出']
usercolumns_merchant_0728 = ['商户编号', '本年交易金额', '商户状态',
                             '本年手续费收入', '本年手续费支出']
df_file_path_0720 = df_file_path_0720[usercolumns_merchant_0720]
df_file_path_0728 = df_file_path_0728[usercolumns_merchant_0728]
merge_df = df_file_path_task.merge(df_file_path_0720, on='商户编号', how='left', suffixes=['_task', '_0720'])
merge_df_2 =merge_df.merge(df_file_path_0728,on='商户编号', how='left', suffixes=['task_0720', '_0728'])
merge_df_2.to_excel('merge_df.xlsx')
