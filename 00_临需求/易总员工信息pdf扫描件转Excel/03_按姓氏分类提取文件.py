import os
import shutil
from pypinyin import pinyin

# 指定源文件夹路径和目标文件夹路径
source_folder = '/Users/fengliang/Desktop/易总文件恢复/待处理文件'
destination_folder = '/Users/fengliang/Desktop/易总文件恢复/按姓氏已分类文件'

# 要排除的特殊文件名列表
exclude_names = {'景福', '北坝', '梓州', '观桥', '营业部',
                 '塔山'
    , '龙树'
    , '梓州'
    , '西平'
    , '八洞'
    , '古井'
    , '刘营'
    , '灵兴'
    , '老马'
    , '芦溪'
    , '立新'
    , '金石'
    , '新鲁'
    , '花园'
    , '永明'
    , '潼川'
    , '北坝'
    , '广化'
    , '上东街'
    , '中新'
    , '富顺'
    , '石安'
    , '新德'
    , '新生'
    , '鲁班'
    , '观桥'
    , '郪江'
    , '景福'
    , '紫河'
    , '乐安'
    , '建平'}

# 确保目标文件夹存在
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# 遍历源文件夹中的所有文件
for filename in os.listdir(source_folder):
    if filename.lower().endswith(('.xls', '.xlsx')):
        # 提取文件名中的姓名（假设文件名为‘姓名.xlsx’）
        base_name = os.path.splitext(filename)[0]

        # 排除特殊文件名
        if base_name in exclude_names:
            print(f'File is in the exclusion list: {filename}')
            continue

        # 仅处理长度不超过 3 个字符的文件
        if len(base_name) <= 3:
            # 获取文件的完整路径
            file_path = os.path.join(source_folder, filename)

            # 提取姓氏的拼音首字母
            # 这里假设文件名的第一个字是姓氏
            surname = base_name[0]  # 取姓氏
            surname_pinyin = pinyin.get(surname, format='strip', delimiter='')  # 获取拼音首字母

            # 创建以拼音首字母命名的文件夹（如果不存在）
            target_folder = os.path.join(destination_folder, surname_pinyin.upper())
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # 移动文件到目标文件夹
            shutil.move(file_path, os.path.join(target_folder, filename))
            print(f'Moved: {filename} to {target_folder}')
        else:
            print(f'File name length exceeds 3 characters: {filename}')
