import os
import PyPDF2

pdf_folder = 'input/PDF/'
pdf_files = os.listdir(pdf_folder)

for i in range(len(pdf_files)):
    text_file = f'{pdf_files[i]}.txt'
    print(pdf_files[i])
    pdf_reader = PyPDF2.PdfFileReader(pdf_folder + pdf_files[i])
    pdf_info = pdf_reader.getDocumentInfo()
    n_pages = pdf_reader.getNumPages()
    for p in range(n_pages):
        pdf_page = pdf_reader.getPage(p)
        pdf_text = pdf_page.extractText()
        print(f'Page no. {p}')
        print(len(pdf_text))
