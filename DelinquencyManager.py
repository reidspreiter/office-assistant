from delinquent_units import DelinquentUnits


def delinquency_manager():
    """
    A wrapper function for a series of DelinquentUnits's methods. 
    These functions work together to read a delinquency report and 
    create individual text messages, individual NTV PDFs, a building 
    walk map, and a master NTV PDF file.
    """
    delinquent_units = DelinquentUnits.DelinquentUnits()
    delinquent_units.prompt_for_delinquency_data()
    delinquent_units.store_delinquency_data()
    
    while True:
        delinquent_units.print_delinquent_units()
        if input("\nDoes this information look correct? (y/n): ") != "n":
            break
        delinquent_units.edit_delinquent_units()

    notice_date, due_date = delinquent_units.get_dates()

    delinquent_units.sort_to_walk()
    delinquent_units.make_map()
    delinquent_units.write_delinquency_texts()
    delinquent_units.get_ntv_pdfs(notice_date, due_date)

    if input("\nType 'SAVE' to keep individual pdf files. Otherwise, press enter: ") != "SAVE":
        delinquent_units.remove_pdfs()