from app.services.PdfService import PdfService

pdf_service = PdfService()

# data/raw/jpgs/irs_forms
# data/raw/jpgs/nar_realtor
# data/raw/jpgs/random
folders = ['data/raw/jpgs/irs_forms', 'data/raw/jpgs/nar_realtor', 'data/raw/jpgs/random']

# pdf_service.consolidate_folders(folders, 'data/raw/jpgs/consolidated')

pdf_service.batch_files_in_folder('data/raw/jpgs/consolidated', 'data/raw/batches', 500, 'image')

# number_of_irs_forms = pdf_service.count_files_in_folder('data/raw/jpgs/irs_forms')
# number_of_nar_realtor = pdf_service.count_files_in_folder('data/raw/jpgs/nar_realtor')
# number_of_random = pdf_service.count_files_in_folder('data/raw/jpgs/random')

# print(number_of_irs_forms)
# print(number_of_nar_realtor)
# print(number_of_random)

# print(number_of_irs_forms + number_of_nar_realtor + number_of_random)
