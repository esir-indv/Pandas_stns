import pandas as pd
import chardet

# 惠商户明细表
merchant_20231231 = '/Users/fengliang/Desktop/惠支付商户统计 20240721/惠商户明细表 20231231.xlsx'
# 对公存款 20231231
merchant_logout_20240630 = '/Users/fengliang/Desktop/惠支付商户统计 20240721/惠商户注销明细表 20240630.xlsx'
# 对公贷款 20240630
# 禁用科学计数法
pd.set_option('display.float_format', lambda x: '%.f' % x)

df_merchant_20231231 = pd.read_excel(merchant_20231231, header=0)

df_merchant_logout_20240630 = pd.read_excel(merchant_logout_20240630, header=0)

# 对所有字符型列去除两边空格
df_merchant_20231231 = df_merchant_20231231.map(lambda x: x.strip() if isinstance(x, str) else x)
df_merchant_logout_20240630 = df_merchant_logout_20240630.map(lambda x: x.strip() if isinstance(x, str) else x)
# 使用 merge 方法进行左连接

merchant_merge = df_merchant_20231231.merge(df_merchant_logout_20240630, how='inner', on=['商户编号'], suffixes=('_20231231' ,'_20240630'))

# 去除重复的记录
merchant_merge = merchant_merge.drop_duplicates()

merchant_merge.to_excel('/Users/fengliang/Desktop/惠支付商户统计 20240721/merchant_merge.xlsx', index=False)

print('合并完成')

