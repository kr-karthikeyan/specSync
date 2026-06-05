from docx import Document

def extract_text_from_docx(file_path: str) -> str:

    document = Document(file_path)
    
    full_text = ""
    
    # A Word document is made of paragraphs
    # This loops through every paragraph in order
    for paragraph in document.paragraphs:
        
        # paragraph.text gives the plain text of that paragraph
        # strip() removes extra spaces or newlines at start/end
        text = paragraph.text.strip()
        
        # Only add non-empty paragraphs
        # (Word docs often have blank paragraphs for spacing)
        if text:
            full_text += text + "\n"
    
    return full_text