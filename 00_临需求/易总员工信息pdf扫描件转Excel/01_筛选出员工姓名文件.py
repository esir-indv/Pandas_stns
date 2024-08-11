import os
import shutil
import re
import stat

# 定义文件夹路径
source_folder = '/Users/fengliang/Desktop/易总文件恢复/待处理文件'
target_folder = '/Users/fengliang/Desktop/易总文件恢复/已分类文件'

# 要排除的关键词
exclude_keywords = ["南路", "西路", "东路", "北路", "总行"]

# 要删除的结尾模式
delete_suffixes = [" (2)", " (3)", " (4)"]
# 正则表达式模式匹配文件名结尾 ' (2)', ' (3)', ' (4)' 以及文件扩展名
pattern = re.compile(r' \((2|3|4)\)\.xls$')
# 正则表达式模式匹配文件名结尾 ' (2)', ' (3)', ' (4)' 以及文件扩展名
pattern_3 = re.compile(r' \((2|3|4)\)\.xlsx$')
# 正则表达式模式匹配文件名以 '_{任意字符}' 结尾
pattern_2 = re.compile(r'_.*\{.*\}$')


# 检查目标文件夹是否存在，如果不存在则创建
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

# 遍历源文件夹中的所有文件
for filename in os.listdir(source_folder):
    filepath = os.path.join(source_folder, filename)
    # 确保处理的是文件而不是子目录
    if os.path.isfile(filepath):
        try:
            # 更改文件权限为可读写
            os.chmod(filepath, stat.S_IWRITE | stat.S_IRUSR | stat.S_IWUSR)
            print(f'Permissions changed for: {filepath}')
        except Exception as e:
            print(f'Error changing permissions: {e} - {filepath}')
            # 检查文件是否以 (1), (2), 或 (3) 结尾，并且是 .xls 或 .xlsx 文件
    if re.search(r'\((1|2|3)\)\.xlsx?$$', filename):
        # 构造完整的文件路径
        filepath = os.path.join(filepath, filename)
        # 删除文件
        os.remove(filepath)
        print(f"Deleted: {filepath}")

    if pattern.search(filename):
        try:
            filepath = os.path.join(source_folder, filename)
            os.remove(filepath)
            print(f'Deleted: {filepath}')
        except PermissionError:
            print(f"Permission denied for file: {filename}. Please check if the file is open or locked.")
        continue
    if pattern_3.search(filename):
        try:
            filepath = os.path.join(source_folder, filename)
            os.remove(filepath)
            print(f'Deleted: {filepath}')
        except PermissionError:
            print(f"Permission denied for file: {filename}. Please check if the file is open or locked.")
        continue
    if pattern_2.search(filename):
        filepath = os.path.join(source_folder, filename)
        try:
            os.remove(filepath)
            print(f'Deleted: {filepath}')
        except PermissionError as e:
            print(f'PermissionError: {e} - {filepath}')
        except Exception as e:
            print(f'Error: {e} - {filepath}')
    if filename.endswith('.et') or filename.endswith('.xlsqm'):
        filepath = os.path.join(source_folder, filename)
        os.remove(filepath)
        print(f'Deleted: {filepath}')
    # 检查文件是否以$开头
    if filename.startswith('$'):
        try:
            os.remove(os.path.join(source_folder, filename))
            print(f"文件 {filename} 已删除。")
        except PermissionError:
            print(f"Permission denied for file: {filename}. Please check if the file is open or locked.")
        continue
    # 删除以 (2)、(3)、(4) 结尾的文件
    if any(filename.endswith(suffix) for suffix in delete_suffixes):
        try:
            os.remove(filepath)
            print(f"文件 {filename} 已删除。")
        except PermissionError:
            print(f"Permission denied for file: {filename}. Please check if the file is open or locked.")
        continue
    if filename.endswith('.xlsx') or filename.endswith('.xls'):
        name = os.path.splitext(filename)[0]

        # 检查文件名中是否包含排除的关键词
        if any(keyword in name for keyword in exclude_keywords):
            #print(f"文件 {filename} 被排除，不会被移动。")
            continue

        # 仅移动文件名长度为两到三个字的文件
        if 2 <= len(name) <= 3:
            print(f"待移动文件:{name}")
            person_folder = os.path.join(target_folder, name)
            if not os.path.exists(person_folder):
                os.makedirs(person_folder)
            try:
                shutil.move(os.path.join(source_folder, filename), os.path.join(person_folder, filename))
            except PermissionError:
                print(f"Permission denied for file: {filename}. Please check if the file is open or locked.")

print("文件分类完成！")

