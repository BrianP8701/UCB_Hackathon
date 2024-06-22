from fast_paperwork.services.pdf_service import PdfService

pdf_service = PdfService()

# Retrieve all PDF paths
paths = pdf_service.get_all_pdf_paths('data/raw/pdfs/irs_forms')

# Debug: Print the paths to ensure they are correct
print("Retrieved PDF paths:", paths)

# Ensure only the first 20 paths are processed
if len(paths) > 20:
    paths = paths[:20]

# Debug: Print the paths that will be processed
print("Processing these PDF paths:", paths)

# Convert and save images
pdf_service.convert_and_save_pdfs_to_images([paths], 'data/raw/jpgs')