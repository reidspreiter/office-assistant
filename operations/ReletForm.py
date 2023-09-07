import os
import fpdf
from operations import MergePDF


def create_relet_form():
    """
    Gathers resident information from the user and 
    writes it to a preexisting relet form template.
    """
    print("\nEnter the resident's first and last name:")
    name = input("> ")
    print("\nEnter the resident's move-out date:")
    move_out_date = input("> ")
    print("\nEnter the resident's *system* Resident Number:")
    resident_number = input("> ")
    print("\nEnter the resident's unit number:")
    unit_number = input("> ")
    print("\nEnter the resident's relet fee:")
    relet_fee = input("> ")

    template = "DO_NOT_DELETE_relet_form_template.pdf"
    overlay = "relet_form_overlay.pdf"
    finished_file = f"Relet Form {name}.pdf"

    pdf = fpdf.FPDF(format = "letter", unit = "pt")
    pdf.add_page()

    pdf.set_font("Arial", style = "", size = 10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(69, 408)
    pdf.cell(0, txt = name)
    pdf.set_xy(69, 453)
    pdf.cell(0, txt = move_out_date)
    pdf.set_xy(69, 499)
    pdf.cell(0, txt = resident_number)
    pdf.set_xy(358, 408)
    pdf.cell(0, txt = unit_number)
    pdf.set_xy(358, 453)
    pdf.cell(0, txt = relet_fee)
    pdf.output(overlay)

    MergePDF.merge_pdfs(template, overlay, finished_file)
    os.system("cls")
    print(f"\nCreated {finished_file}")
