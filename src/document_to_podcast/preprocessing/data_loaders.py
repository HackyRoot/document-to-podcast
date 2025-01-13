import os
import PyPDF2

from docx import Document
from loguru import logger
from streamlit.runtime.uploaded_file_manager import UploadedFile
from markitdown import MarkItDown


def load_pdf(pdf_file: str | UploadedFile) -> str | None:
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        return "\n".join(page.extract_text() for page in pdf_reader.pages)
    except Exception as e:
        logger.exception(e)
        return None


def load_txt(txt_file: str | UploadedFile) -> str | None:
    try:
        if isinstance(txt_file, UploadedFile):
            return txt_file.getvalue().decode("utf-8")
        else:
            with open(txt_file, "r") as file:
                return file.read()
    except Exception as e:
        logger.exception(e)
        return None


def load_docx(docx_file: str | UploadedFile) -> str | None:
    try:
        docx_reader = Document(docx_file)
        return "\n".join(paragraph.text for paragraph in docx_reader.paragraphs)
    except Exception as e:
        logger.exception(e)
        return None


def load_file(file: str | UploadedFile) -> str | None:
    """
    Loads the content of a file or URL and converts it to markdown.

    Args:
        file (str | UploadedFile): The path to the file, a URL.

    Returns:
        str | None: The markdown text content, or None if an error occurs.
    """
    try:
        markdown_converter = MarkItDown()
        if isinstance(file, str):  # for URL and filepath
            if not os.path.exists(file):
                logger.error(f"File not found: {file}")
                return None
            markdown_content = markdown_converter.convert(file)
        elif isinstance(file, UploadedFile):
            markdown_content = markdown_converter.convert(str(file))
        else:
            logger.error(f"Unsupported file type: {type(file)}")
            return None
        markdown_text = markdown_content.text_content
        return markdown_text    
    except Exception as e:
        logger.exception(f"An error occurred while loading the file: {e}")
        return None
