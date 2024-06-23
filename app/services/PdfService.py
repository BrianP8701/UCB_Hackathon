from typing import List, Tuple
from pdf2image import convert_from_path
from PyPDF2 import PdfReader, PdfWriter
from os.path import isfile
import requests
import os
import fitz
from concurrent.futures import ThreadPoolExecutor, as_completed
import shutil
import io

from app.utils import get_path_from_file_id

class PdfService:
    
    @classmethod
    def get_file_object(cls, file_path: str) -> str:
        """
        Get the file object from a file path.
        """
        if not isfile(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist.")
        return file_path

    @classmethod
    def convert_pdf_to_images(cls, file_path: str) -> List[bytes]:
        """
        Convert a PDF file to a list of images as bytes.
        """
        if not file_path.endswith('.pdf'):
            raise ValueError(f"File {file_path} is not a PDF.")

        images = convert_from_path(get_path_from_file_id(file_path), dpi=300, output_folder=None, fmt='jpeg')
        image_bytes = []
        for image in images:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG')
            image_bytes.append(img_byte_arr.getvalue())
        return image_bytes

    @classmethod
    def get_all_pdf_paths(cls, folder_path: str) -> List[str]:
        """
        Get all PDF paths from a given folder path.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder {folder_path} does not exist.")
        
        pdf_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
        return pdf_paths

    @classmethod
    def convert_and_save_pdfs_to_images(cls, pdf_paths: List[List[str]], output_folder: str) -> None:
        """
        Convert a list of lists of PDF paths to images concurrently and save them to a given folder.
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        def convert_and_save(pdf_path: str) -> None:
            try:
                images = cls.convert_pdf_to_images(pdf_path)
                for i, image in enumerate(images):
                    print(f"Saving image {i} from {pdf_path}")
                    image_path = os.path.join(output_folder, f"{os.path.basename(pdf_path).replace('.', '-')}_{i}.jpeg")
                    image.save(image_path)
            except Exception as e:
                print(f"Error processing {pdf_path}: {e}")

        # Flatten the list of lists into a single list of paths
        flat_list = [item for sublist in pdf_paths for item in sublist]
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(convert_and_save, pdf_path) for pdf_path in flat_list]
            for future in as_completed(futures):
                future.result() 

    @classmethod
    def is_pdf_corrupted(cls, file_path: str) -> bool:
        """
        Check if a PDF file is corrupted.
        """
        try:
            with open(file_path, 'rb') as f:
                pdf = PdfReader(f)
                len(pdf.pages)
                return False
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return True

    @classmethod
    def remove_corrupted_pdfs(cls, folder_path: str) -> None:
        """
        Remove corrupted PDF files from a specified folder.
        """
        pdf_paths = cls.get_all_pdf_paths(folder_path)
        for pdf_path in pdf_paths:
            if cls.is_pdf_corrupted(pdf_path):
                os.remove(pdf_path)
                print(f"Removed corrupted PDF: {pdf_path}")

    @classmethod
    def download_pdfs(cls, pdf_urls: List[str], folder_path: str, file_name: str) -> None:
        """
        Download PDF files from a list of URLs and save them to a folder.
        """
        count = 0
        for pdf_url in pdf_urls:
            response = requests.get(pdf_url)
            with open(os.path.join(folder_path, f"{file_name}_{count}.pdf"), 'wb') as file:
                file.write(response.content)
            count += 1

    @classmethod
    def get_form_fields_and_rectangles(cls, pdf_path: str) -> Tuple[int, List]:
        """
        Get the form fields and corresponding rectangles from a PDF file.
        """
        doc = fitz.open(pdf_path)
        form_fields = []

        for page in doc:
            for field in page.widgets():
                form_fields.append(field.rect)

        return len(form_fields), form_fields

    @classmethod
    def count_files_in_folder(cls, folder_path: str) -> int:
        """
        Count the number of files in a given folder.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder {folder_path} does not exist.")
        return len(os.listdir(folder_path))

    @classmethod
    def batch_files_in_folder(cls, folder_path: str, batch_folder_path: str, batch_size: int, batch_name: str) -> None:
        """
        Create batches of files from a folder, each batch containing up to 'batch_size' files and save them to a specified batch folder path.
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder {folder_path} does not exist.")
        if not os.path.exists(batch_folder_path):
            os.makedirs(batch_folder_path, exist_ok=True)

        files = os.listdir(folder_path)
        batch_count = 0
        
        for i in range(0, len(files), batch_size):
            batch_folder = os.path.join(batch_folder_path, f"{batch_name}_{batch_count}")
            os.makedirs(batch_folder, exist_ok=True)
            for file in files[i:i + batch_size]:
                shutil.move(os.path.join(folder_path, file), batch_folder)
            batch_count += 1

    @classmethod
    def consolidate_folders(cls, source_folder_paths: List[str], destination_folder_path: str) -> None:
        """
        Consolidate files from multiple folders into a single folder.
        """
        if not os.path.exists(destination_folder_path):
            os.makedirs(destination_folder_path)
        
        for source_folder in source_folder_paths:
            if not os.path.exists(source_folder):
                raise FileNotFoundError(f"Source folder {source_folder} does not exist.")
            for item in os.listdir(source_folder):
                source = os.path.join(source_folder, item)
                destination = os.path.join(destination_folder_path, item)
                if os.path.isdir(source):
                    shutil.copytree(source, destination)
                else:
                    shutil.copy(source, destination)

    @classmethod
    def merge_pdfs(cls, pdf_bytes_list: List[bytes]) -> bytes:
        """
        Merge a list of PDF files (in bytes) into a single PDF and return the merged PDF as bytes.
        """
        pdf_writer = PdfWriter()
        
        for pdf_bytes in pdf_bytes_list:
            pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)
        
        output_stream = io.BytesIO()
        pdf_writer.write(output_stream)
        return output_stream.getvalue()
