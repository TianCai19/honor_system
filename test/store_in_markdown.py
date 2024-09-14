import os

# 跳过这些文件夹
WHITELIST_DIRS = ['data', 'chathistory']  # 替换为你想跳过的目录名称

def is_whitelisted(directory):
    """
    判断文件夹是否在白名单中
    """
    for whitelist_dir in WHITELIST_DIRS:
        if whitelist_dir in directory:
            return True
    return False

def list_files_in_project(start_path, output_md):
    with open(output_md, 'w', encoding='utf-8') as md_file:
        md_file.write("# Project File Structure with File Contents\n\n")
        for root, dirs, files in os.walk(start_path):
            # 跳过白名单中的文件夹
            if is_whitelisted(root):
                continue
            
            # 跳过隐藏文件夹（以'.'开头的文件夹）
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            level = root.replace(start_path, '').count(os.sep)
            indent = ' ' * 4 * level
            md_file.write(f"{indent}- **{os.path.basename(root)}/**\n")
            sub_indent = ' ' * 4 * (level + 1)

            for f in files:
                # 跳过隐藏文件（以'.'开头的文件）
                if f.startswith('.'):
                    continue

                file_path = os.path.join(root, f)
                md_file.write(f"{sub_indent}- {f}\n{sub_indent}Path: `{file_path}`\n")

                # 读取文件内容并写入 Markdown 文件
                try:
                    with open(file_path, 'r', encoding='utf-8') as file_content:
                        content = file_content.read()
                        md_file.write(f"{sub_indent}**Content:**\n")
                        md_file.write(f"```text\n{sub_indent}{content}\n```\n\n")
                except Exception as e:
                    md_file.write(f"{sub_indent}**Error reading file:** {str(e)}\n\n")

if __name__ == "__main__":
    project_directory = '.'  # 当前目录，也可以指定其他目录
    output_markdown = 'project_structure_with_contents.md'  # 输出 Markdown 文件的名称
    list_files_in_project(project_directory, output_markdown)
    print(f"文件结构和内容已保存到 {output_markdown}")