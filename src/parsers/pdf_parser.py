import fitz

def extract_text_from_pdf(file_path: str) -> str:

    document = fitz.open(file_path)

    full_text = ""

    for page_number, page in enumerate(document):
        
        # Extract all readable text from this single page
        page_text = page.get_text()
        
        # Add a label so we know which page the text came from
        full_text += f"\n--- Page {page_number + 1} ---\n"
        
        # Append this page's text to our collection
        full_text += page_text
    
    # Close the document — good practice to free up memory
    document.close()
    
    return full_text