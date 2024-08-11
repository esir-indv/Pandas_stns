import pandas as pd

# 商户交易明细表 6 月
file_path = '/Users/fengliang/Documents/Pandas_stns/01_惠商户/01_惠商户分类分级记差异化费率化试点/01_白名单匹配/白名单申请表_第二批录入_20240728.xlsx'
file_path_oa = '/Users/fengliang/Documents/Pandas_stns/01_惠商户/01_惠商户分类分级记差异化费率化试点/01_白名单匹配/白名单申请_OA_录入.xlsx'
file_path_merchant_0720 = '/Users/fengliang/Documents/Pandas_stns/01_惠商户/01_惠商户分类分级记差异化费率化试点/01_白名单匹配/商户分户统计表-0720.csv'

try:
    df_white_list = pd.read_excel(file_path)
    df_merchant_0720 = pd.read_csv(file_path_merchant_0720, encoding='gbk')
    df_white_list_oa = pd.read_excel(file_path_oa)
except Exception as e:
    print(e)


# 定义一个函数来根据资金留存率确定费率
def calculate_fee_rate(x):
    if x < 0.1:
        return 0.0025
    elif 0.1 <= x < 0.2:
        return 0.002
    elif 0.2 <= x < 0.3:
        return 0.0015
    elif 0.3 <= x < 0.4:
        return 0.001
    else:
        return 0


print(df_merchant_0720.columns)
usercolumns_merchant = ['商户编号', '机构号', '机构名称', '商户名称', '商户简称', '本月交易金额','本年交易金额', '本月交易笔数','商户种类', '商户状态','本年手续费收入','本年手续费支出', '结算账户年日均存款余额', '年日均贷款余额']
df_merchant_0720 = df_merchant_0720[usercolumns_merchant]
df_merchant_0720['资金留存率'] = df_merchant_0720['结算账户年日均存款余额'] / df_merchant_0720['本年交易金额']
# 应用函数并创建新列 '费率'
df_merchant_0720['费率'] = df_merchant_0720['资金留存率'].apply(calculate_fee_rate)
print(df_merchant_0720.columns)
df_white_list['商户编号'] = df_white_list['商户编号'].astype(str)
df_white_list_oa['商户编号'] = df_white_list_oa['商户编号'].astype(str)

df_merchant_0720['商户编号'] = df_merchant_0720['商户编号'].astype(str)

merge_df = df_white_list.merge(df_merchant_0720, on='商户编号', how='left')
merge_df_oa = df_white_list_oa.merge(df_merchant_0720, on='商户编号', how='left')

merge_df.to_excel('merge_df.xlsx')
merge_df_oa.to_excel('merge_df_oa.xlsx')



"""
import pandas as pd

# 读取 Excel 文件
file_path = "/mnt/data/sample_data.xlsx"
df = pd.read_excel(file_path)

# 筛选符合条件的记录：机构列为“营业部”且层级列不为“高值”
filtered_df = df[(df["机构列"] == "营业部") & (df["层级列"] != "高值")]

# 计算符合条件的记录数量
count = filtered_df.shape[0]

count

"""


