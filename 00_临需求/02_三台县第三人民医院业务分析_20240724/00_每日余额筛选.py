import pandas as pd

df_2023 = '/Users/fengliang/Documents/workspace/Pandas&SCNS/惠商户差异化收费试点/三台县第三人民医院业务分析_20240724/三台县第三人民医院业务分析表/三台县三医院23 年存款信息.xlsx'

df_2024 = '/Users/fengliang/Documents/workspace/Pandas&SCNS/惠商户差异化收费试点/三台县第三人民医院业务分析_20240724/三台县第三人民医院业务分析表/三台县三医院 24 年存款信息.xlsx'

# 禁用科学计数法
pd.set_option('display.float_format', lambda x: '%.f' % x)

df_Dpt_2023 = pd.read_excel(df_2023)

df_Dpt_2024 = pd.read_excel(df_2024)

# 对所有字符型列去除两边空格
df_Dpt_2023 = df_Dpt_2023.map(lambda x: x.strip() if isinstance(x, str) else x)

df_Dpt_2024 = df_Dpt_2024.map(lambda x: x.strip() if isinstance(x, str) else x)

# 根据 'group' 列删除重复项并保留最后一个值
df_unique_2023 = df_Dpt_2023.drop_duplicates(subset='交易日期', keep='last')
df_unique_2024 = df_Dpt_2024.drop_duplicates(subset='交易日期', keep='last')

df_unique_2023.to_excel('/Users/fengliang/Desktop/df_unique_2023.xlsx', index=False)
df_unique_2024.to_excel('/Users/fengliang/Desktop/df_unique_2024.xlsx', index=False)

