import os
import re
import stat

# 定义文件夹路径
source_folder = '/Users/fengliang/Desktop/易总文件恢复/待处理文件'
target_folder = '/Users/fengliang/Desktop/易总文件恢复/已分类文件'

# 要排除的关键词
exclude_keywords = ["南路", "西路", "东路", "北路", "总行"]

"""
修改可执行权限
"""


def change_permissions_with_sudo(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                # 检查文件是否只读
                file_stat = os.stat(file_path)
                if not bool(file_stat.st_mode & stat.S_IWUSR):
                    print(f"Changing permissions for {file_path}")
                    # 构造并执行 sudo chmod 命令
                    command = f"sudo chmod u+rw '{file_path}'"
                    os.system(command)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")


# 替换为你要处理的目录路径
change_permissions_with_sudo(source_folder)
"""
修改文件名中的空格
"""
def remove_spaces_in_filenames(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if " " in file_name:
                # 构造新的文件名
                new_file_name = file_name.replace(" ", "")
                old_file_path = os.path.join(root, file_name)
                new_file_path = os.path.join(root, new_file_name)
                try:
                    # 重命名文件
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed: '{old_file_path}' to '{new_file_path}'")
                except Exception as e:
                    print(f"Error renaming '{old_file_path}': {e}")


# 替换为你要处理的目录路径
remove_spaces_in_filenames(source_folder)

# 遍历源文件夹中的所有文件
for filename in os.listdir(source_folder):
    filepath = os.path.join(source_folder, filename)
    # 检查文件是否以$开头
    if filename.startswith('$'):
        try:
            os.remove(os.path.join(source_folder, filename))
            print(f"文件 {filename} 已删除。")
        except PermissionError:
            print(f"Permission denied for file: {filename}. Please check if the file is open or locked.")
        continue
    # 检查文件是否以et、xlsqm结尾
    if filename.endswith('.et') or filename.endswith('.xlsqm'):
        try:
            os.remove(os.path.join(source_folder, filename))
            print(f"文件 {filename} 已删除。")
        except PermissionError:
            print(f"Permission denied for file: {filename}. Please check if the file is open or locked.")
        continue
"""
删除文件名以多个 (数字) 结尾的文件，例如 游巴蜀报名表(4)(3)，使用正则表达式来匹配这种模式。
"""

# 正则表达式模式，用于匹配文件名以一个 (数字) 结尾
pattern = re.compile(r'\(\d+\)\.(xls|xlsx)$', re.IGNORECASE)

# 遍历文件夹中的所有文件
for filename in os.listdir(source_folder):
    # 打印文件名以帮助调试
    print(f'Found file: {filename}')

    # 检查文件扩展名是否为 .xls 或 .xlsx
    if filename.lower().endswith(('.xls', '.xlsx')):
        # 打印匹配信息
        print(f'Checking file: {filename}')

        # 检查文件名是否符合正则表达式模式
        if pattern.search(filename):
            # 获取完整文件路径
            file_path = os.path.join(source_folder, filename)
            # 打印将要删除的文件路径
            print(f'Deleting file: {file_path}')

            # 删除文件
            os.remove(file_path)
        else:
            print(f'File does not match pattern: {filename}')
    else:
        print(f'File is not an xls or xlsx: {filename}')

# 正则表达式模式，用于匹配文件名以 _{UUID} 结尾
pattern = re.compile(r'_\{[0-9a-fA-F\-]{36}\}\.(xls|xlsx)$', re.IGNORECASE)

# 遍历文件夹中的所有文件
for filename in os.listdir(source_folder):
    # 检查文件是否符合正则表达式模式
    if pattern.search(filename):  # 使用 search 以查找模式
        # 获取完整文件路径
        file_path = os.path.join(source_folder, filename)
        # 删除文件
        os.remove(file_path)
        print(f'Deleted: {file_path}')
    else:
        print(f'File does not match pattern: {filename}')

# 正则表达式模式，用于匹配以 1 到 800 之间的数字开头的文件名
number_pattern = re.compile(r'^([1-7][0-9]{0,2}|800)(.*\.(xls|xlsx))$', re.IGNORECASE)

# 正则表达式模式，用于匹配以年份开头的文件名（例如：2020年）
year_pattern = re.compile(r'^\d{4}年.*\.(xls|xlsx)$', re.IGNORECASE)

# 遍历文件夹中的所有文件
for filename in os.listdir(source_folder):
    if year_pattern.match(filename):
        # 保留以年份开头的文件名
        print(f'File is year-prefixed and retained: {filename}')
    elif number_pattern.match(filename):
        # 提取新文件名（去掉数字开头部分）
        match = number_pattern.match(filename)
        new_filename = match.group(2)
        # 获取完整文件路径
        old_file_path = os.path.join(source_folder, filename)
        new_file_path = os.path.join(source_folder, new_filename)
        # 重命名文件
        os.rename(old_file_path, new_file_path)
        print(f'Renamed: {filename} to {new_filename}')
    else:
        print(f'File does not match any pattern: {filename}')


# 正则表达式模式，用于匹配以一个或两个数字开头的文件名
number_pattern = re.compile(r'^\d{1,2}(.*\.(xls|xlsx))$', re.IGNORECASE)

# 遍历文件夹中的所有文件
for filename in os.listdir(source_folder):
    # 检查是否匹配一个或两个数字开头的文件名
    if number_pattern.match(filename):
        base_name = filename.rsplit('.', 1)[0]  # 去掉扩展名
        if len(base_name) < 8:
            match = number_pattern.match(filename)
            new_filename = match.group(1)
            # 获取完整文件路径
            old_file_path = os.path.join(source_folder, filename)
            new_file_path = os.path.join(source_folder, new_filename)
            # 重命名文件
            os.rename(old_file_path, new_file_path)
            print(f'Renamed: {filename} to {new_filename}')
        else:
            print(f'File does not need renaming (length >= 6): {filename}')
    else:
        print(f'File does not match any pattern: {filename}')