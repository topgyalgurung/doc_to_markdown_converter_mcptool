import os
from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Absolute or relative path to a PDF or DOCX file to convert"),
) -> str:
    """Convert a PDF or DOCX file to markdown-formatted text.

    Reads the file at the given path and converts its contents to markdown.
    Supports .pdf and .docx file formats.

    When to use:
    - When you have a local file path to a document and need its text content
    - When you need to extract and process text from a PDF or Word document

    When NOT to use:
    - When you already have the file contents as bytes (use binary_document_to_markdown instead)
    - When the file is not a PDF or DOCX

    Examples:
    >>> document_path_to_markdown("/path/to/report.pdf")
    "# Report Title\\n\\nContent..."
    >>> document_path_to_markdown("/path/to/document.docx")
    "# Document Title\\n\\nContent..."
    """
    _, ext = os.path.splitext(file_path)
    file_type = ext.lstrip(".").lower()
    if file_type not in ("pdf", "docx"):
        raise ValueError(f"Unsupported file type '{ext}'. Must be .pdf or .docx.")
    with open(file_path, "rb") as f:
        binary_data = f.read()
    return binary_document_to_markdown(binary_data, file_type)
