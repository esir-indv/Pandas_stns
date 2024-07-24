import pandas as pd
import chardet

# 对公存款 20240630
Dpt_20240630 = '/Users/fengliang/Documents/workspace/Pandas&SCNS/惠商户差异化收费试点/卫生院存贷情况统计源/对公存款20240630.xlsx'
# 对公存款 20231231
Dpt_20231231 = '/Users/fengliang/Documents/workspace/Pandas&SCNS/惠商户差异化收费试点/卫生院存贷情况统计源/对公存款20231231.xlsx'
# 对公贷款 20240630
Loan_20240630 = '/Users/fengliang/Documents/workspace/Pandas&SCNS/惠商户差异化收费试点/卫生院存贷情况统计源/对公贷款20240630.xlsx'

df_Dpt_20240630 = pd.read_excel(Dpt_20240630, header=0, dtype={'账户名称': str, '账户性质': str})

df_Dpt_20231231 = pd.read_excel(Dpt_20231231, header=0, dtype={'账户名称': str, '账户性质': str})

df_Loan_20240630 = pd.read_excel(Loan_20240630, header=0, dtype={'账户名称': str, '账户性质': str})


# 对所有字符型列去除两边空格
df_Dpt_20240630 = df_Dpt_20240630.map(lambda x: x.strip() if isinstance(x, str) else x)
df_Dpt_20231231 = df_Dpt_20231231.map(lambda x: x.strip() if isinstance(x, str) else x)
df_Loan_20240630 = df_Loan_20240630.map(lambda x: x.strip() if isinstance(x, str) else x)



# 使用 merge 方法进行左连接
Dpt_merge = df_Dpt_20240630.merge(df_Dpt_20231231, how='left', on=['账户名称', '账户性质'])
# 连接贷款
Dpt_merge = Dpt_merge.merge(df_Loan_20240630, on='账户名称', how='left', suffixes=(None, '_loan_20240630'))
# 去除重复的记录
Dpt_merge = Dpt_merge.drop_duplicates()
# # 输出excel
Dpt_merge.to_excel('Dpt_merge.xlsx', index=False)
