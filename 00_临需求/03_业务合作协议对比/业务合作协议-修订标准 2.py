from docx import Document
import difflib
import pdfkit





def get_text_from_docx(doc_path):
    doc = Document(doc_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)


def compare_documents(doc1_path, doc2_path):
    text1 = get_text_from_docx(doc1_path)
    text2 = get_text_from_docx(doc2_path)

    diff = difflib.HtmlDiff(wrapcolumn=80).make_file(text1.splitlines(), text2.splitlines(), fromdesc='原始文档——银行',
                                                     todesc='修订文档-公司')

    # Remove legend and line numbers from the generated HTML
    diff = diff.replace('<table class="diff" id="difflib_chg_to0__top"', '<table class="diff"')
    diff = diff.replace('<thead>', '<thead style="display:none">')
    diff = diff.replace('<td class="diff_next">', '<td class="diff_next" style="display:none">')
    diff = diff.replace('<th class="diff_next">', '<th class="diff_next" style="display:none">')

    return diff


doc1_path = '/Users/fengliang/Desktop/业务合作协议修订对比/业务合作协议-银行.docx'
doc2_path = '/Users/fengliang/Desktop/业务合作协议修订对比/业务合作协议-公司.docx'


diff_result = compare_documents(doc1_path, doc2_path)

# 保存 HTML 文件（可选）
with open('业务合作协议-修订标注.html', 'w', encoding='utf-8') as file:
    file.write(diff_result)


