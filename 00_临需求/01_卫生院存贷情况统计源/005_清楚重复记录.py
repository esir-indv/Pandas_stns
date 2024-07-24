import pandas as pd
import chardet

# 惠商户明细表
df_path = '/Users/fengliang/Desktop/惠支付商户统计 20240721/副本卫生类账户存贷情况统计_20240721.xlsx'

# 禁用科学计数法
pd.set_option('display.float_format', lambda x: '%.f' % x)

df = pd.read_excel(df_path, header=0)

# 删除重复记录
df = df.drop_duplicates()

df.to_csv('/Users/fengliang/Desktop/惠支付商户统计 20240721/drop_duplicates.csv', index=False)
