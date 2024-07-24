import difflib
from docx import Document
from weasyprint import HTML


# 读取两个 Word 文档
def read_docx(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


# 比较两个文档的差异并生成 HTML
def generate_diff_html(doc1, doc2):
    d = difflib.HtmlDiff()
    lines1 = doc1.splitlines()
    lines2 = doc2.splitlines()
    html_diff = d.make_file(lines1, lines2, fromdesc='Document 1', todesc='Document 2')
    return html_diff


# 将 HTML 写入 PDF 文件
def write_html_to_pdf(html_content, output_file):
    HTML(string=html_content).write_pdf(output_file)


# 主函数
def main(doc1_path, doc2_path, output_pdf_path):
    doc1_text = read_docx(doc1_path)
    doc2_text = read_docx(doc2_path)
    html_diff = generate_diff_html(doc1_text, doc2_text)
    write_html_to_pdf(html_diff, output_pdf_path)


# 使用示例
doc1_path = '/Users/fengliang/Desktop/业务合作协议修订对比/业务合作协议-银行.docx'
doc2_path = '/Users/fengliang/Desktop/业务合作协议修订对比/业务合作协议-公司.docx'
output_pdf_path = '/Users/fengliang/Desktop/业务合作协议修订对比/业务合作协议-公司.pdf'

main(doc1_path, doc2_path, output_pdf_path)
