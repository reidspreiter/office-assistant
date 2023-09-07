from PyPDF2 import PdfWriter, PdfReader, PdfMerger


def merge_pdfs(template, overlay, result):
    """
    Merges an edited overlay pdf on top of a preexisting 
    template pdf and saves the resulting file.

    Parameters:
        template (str): The name of a template file.
        overlay (str): The name of an overlay file.
        result (str): The name to save the resulting file as.
    """
    template_pdf = PdfReader(open(template, "rb"))
    overlay_pdf = PdfReader(open(overlay, "rb"))

    template_pdf.pages[0].merge_page(overlay_pdf.pages[0])

    finished_pdf = PdfWriter()
    finished_pdf.add_page(template_pdf.pages[0])
    finished_pdf.write(open(result, "wb"))
    finished_pdf.close()


def combine_pdf_pages(pdf_pages, result):
    """
    Combines individual pdf files into a single document 
    and saves the resulting file.

    Parameters:
        pdf_pages (str list): A list of file names to combine.
        result (str): The name to save the resulting file as.
    """
    merger = PdfMerger()
    for page in pdf_pages:
        merger.append(page)

    merger.write(open(result, "wb"))
    merger.close()