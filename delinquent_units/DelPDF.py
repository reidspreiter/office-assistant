import fpdf
from operations import MergePDF


def create_ntv_pdf(unit, notice_date, due_date, ntv_pdfs):
    """
    Creates an NTV PDF and stores the file name in ntv_pdfs.

    Parameters:
        unit (DelUnit object): A delinquent unit's information.
        notice_date (str): The current date.
        due_date (str): The date three days from now, excluding 
                        weekends and recognized holidays.
        ntv_pdfs (str list): A list of NTV PDF file names.
    """
    template = "DO_NOT_DELETE_delinquency_template.pdf"
    overlay = "temp_overlay.pdf"
    finished_file = f"3 Day NTV {unit.unit_number}{unit.initials}.pdf"

    pdf = fpdf.FPDF(format = "letter", unit = "pt")
    pdf.add_page()
    pdf.set_font("Arial", style = "B", size = 7.9)
    pdf.set_text_color(255, 0, 0)

    pdf.set_xy(68, 158)
    pdf.cell(0, txt = unit.occupants)
    pdf.set_xy(426, 158)
    pdf.cell(0, txt = notice_date)
    pdf.set_xy(404, 187)
    pdf.cell(0, txt = unit.guarantor)

    pdf.set_font("Arial", style = "", size = 7.9)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(68, 187)
    pdf.cell(0, txt = unit.address)

    pdf.set_font("Arial", style = "B", size = 10)
    pdf.set_text_color(255, 0, 0)
    pdf.set_xy(49, 274)
    pdf.cell(0, txt = unit.balance_in_words)

    pdf.set_font("Arial", style = "", size = 8.9)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(328, 288)
    pdf.cell(0, txt = unit.address)

    pdf.set_font("Arial", style = "B", size = 10)
    pdf.set_text_color(255, 0, 0)
    pdf.set_xy(150, 338)
    pdf.cell(0, txt = due_date)

    pdf.output(overlay)
    MergePDF.merge_pdfs(template, overlay, finished_file)
    ntv_pdfs.append(finished_file)