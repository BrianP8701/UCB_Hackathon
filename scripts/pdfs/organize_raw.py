from app.services.pdf_service import PdfService
import os

pdf_service = PdfService()

pdf_paths = pdf_service.get_all_pdf_paths('data/raw/pdfs/irs_forms')

pdf_service.convert_and_save_pdfs_to_images([pdf_paths], 'data/raw/jpgs/irs_forms')
