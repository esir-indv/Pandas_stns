from docx import Document
import difflib


def get_text_from_docx(doc_path):
    doc = Document(doc_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)


def compare_documents(doc1_path, doc2_path):
    text1 = get_text_from_docx(doc1_path)
    text2 = get_text_from_docx(doc2_path)

    diff = difflib.unified_diff(text1.splitlines(), text2.splitlines(), lineterm='')
    return '\n'.join(diff)


doc1_path = '/Users/fengliang/Desktop/业务合作协议修订对比/业务合作协议-银行.docx'
doc2_path = '/Users/fengliang/Desktop/业务合作协议修订对比/业务合作协议-公司.docx'

diff_result = compare_documents(doc1_path, doc2_path)

# 保存输出到文件
with open('diff_result.txt', 'w', encoding='utf-8') as file:
    file.write(diff_result)
