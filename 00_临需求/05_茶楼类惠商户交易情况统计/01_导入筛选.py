import pandas as pd

# 商户交易明细表 6 月
file_path = '/Users/fengliang/Documents/Pandas_stns/00_临需求/05_茶楼类惠商户交易情况统计/商户交易明细表202406.csv'
file_path_merchant = '/Users/fengliang/Documents/Pandas_stns/00_临需求/05_茶楼类惠商户交易情况统计/商户分户统计表-0630.csv'
# 惠支付商户分户表
try:
    df = pd.read_csv(file_path, encoding='gbk')
    df_merchant = pd.read_csv(file_path_merchant, encoding='gbk')
except Exception as e:
    print(e)
# 打印列名
print("商户交易明细表字段：", df.columns)
print("商户分户表字段：", df_merchant.columns)

usecolumns = ['机构号', '机构名称', '商户号', '商户名称', '商户种类', '交易时间', '订单金额', '交易手续费', '支付渠道',
              '交易单号']
usercolumns_merchant = ['商户编号', '商户名称', '商户简称', '商户性质', '商户类型', '商户种类', '商户状态', '行业类别',
                        '行业子类', '结算账户年日均存款余额', '年日均贷款余额']
df = df[usecolumns]
df_merchant = df_merchant[usercolumns_merchant]

print("商户交易明细表字段_使用", df.columns)
print("商户分户统计表字段_使用", df_merchant.columns)
# 查看记录数
record_count = len(df)
print(f"商户交易明细表总记录数：{record_count}")
# 使用 unique() 方法查看商户类别字段中有哪些种类
unique_categories = df['商户种类'].unique()
print("商户类别字段中的种类有：", unique_categories)
unique_categories_TradDate = df['交易时间'].unique()
print("交易时间字段中有：", unique_categories_TradDate)
# 查看行业类别种类
unique_categories_hylb = df_merchant['行业类别'].unique()
print("行业类别种类有：", unique_categories_hylb)
# 查看行业字类分类
unique_categories_hyzlb = df_merchant['行业子类'].unique()
print("商户子类别种类有：", unique_categories_hyzlb)
# 使用 value_counts() 方法查看每种商户类别的计数
category_counts = df['商户种类'].value_counts()
print("\n每种商户类别的计数：")
print(category_counts)
# 筛选商户交易明细表中订单金额大于等于 2000的记录
filtered = df[df['订单金额'] >= 2000]
print(f"总记录数：{len(filtered)}")
# 筛选商户分户统计表中行业类别
filtered_merchant_type = df_merchant[df_merchant['行业类别'].isin(['休闲娱乐业', '餐饮业'])]
print(filtered_merchant_type['行业类别'].unique())
print(filtered_merchant_type['行业子类'].unique())

filtered_merchant_type = filtered_merchant_type[
    filtered_merchant_type['行业子类'].isin(['休闲饮品场所、酒吧、咖啡厅、茶馆', '按摩足疗店', '保健、美容及洗浴服务'])]

print(filtered_merchant_type['行业类别'].unique())
print(filtered_merchant_type['行业子类'].unique())

filtered_20_tmp = filtered.head(20)
filtered_merchant_type_20_tmp = filtered_merchant_type.head(20)
# 查看前 20 条数据
filtered_20_tmp.to_excel('filtered_20_tmp.xlsx')
filtered_merchant_type_20_tmp.to_excel('filtered_merchant_type_20_tmp.xlsx')

# 两表开始左连接
merge_df = filtered.merge(filtered_merchant_type, left_on='商户号', right_on='商户编号', how='inner',
                          suffixes=('', '_merge'))
merge_df.to_excel('merge_df.xlsx')