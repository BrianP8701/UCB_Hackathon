import fitz
import os

def get_form_fields_and_rectangles(pdf_path):
    doc = fitz.open(pdf_path)
    form_fields = []

    for page in doc:
        for field in page.widgets():
            form_fields.append(field.rect)

    return len(form_fields), form_fields


folder_path = 'data/raw'
pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
number_of_pdfs_with_forms = 0

for pdf_file in pdf_files:
    pdf_path = os.path.join(folder_path, pdf_file)
    num_fields, fields = get_form_fields_and_rectangles(pdf_path)
    if num_fields > 0:
        number_of_pdfs_with_forms += 1
    print(f"File: {pdf_file}, Number of form fields: {num_fields}, Fields: {fields}")

print(f"Number of PDFs with forms: {number_of_pdfs_with_forms}")