import os

from operations import MergePDF
from unit_numbers import UnitNumbers
from delinquent_units import DelUnit
from delinquent_units import DelPDF
from delinquent_units import DelDates

class DelinquentUnits:
    """
    A class representing a list of delinquent units.

    Attributes:
        del_units (dict): A dict mapping delinquent units with unit numbers.
        sorted_del_units (DelinquencyUnit list): A list of delinquent units.
        ntv_pdfs (str list): A list of ntv file names.
        del_unit_numbers (UnitNumbers class): A list of unit numbers.
        del_data_file_name (str): The name of the delinquency data file.
        del_texts_file_name (str): The name of the created texts file.
        master_del_file_name (str): The name of the master delinquency file.
    """


    def __init__(self):
        """
        Initializes a DelinquentUnits object.
        """
        self.del_units = {}
        self.sorted_del_units = []
        self.ntv_pdfs = []
        self.del_unit_numbers = UnitNumbers.UnitNumbers()
        self.del_data_file_name = "delinquency.txt"
        self.del_texts_file_name = "Delinquency Texts.txt"
        self.master_del_file_name = "Master Delinquency File.pdf"


    def back(self):
        """
        Returns the last unit number in del_unit_numbers.

        Return:
            (int): The last unit number in del_unit_numbers.
        """
        return self.del_unit_numbers.back()
    

    def sort_to_walk(self):
        """
        Sorts del_unit_numbers in an order that 
        is most ideal to walk in real life, then 
        sorts del_units's values in a new list 
        based on the most ideal walk path.
        """
        self.del_unit_numbers.sort_to_walk()
        for unit_number in self.del_unit_numbers.unit_numbers:
            self.sorted_del_units.append(self.del_units.get(unit_number))


    def make_map(self):
        """
        Calls UnitNumbers make_map() function and
        appends the map_file_name to ntv_pdfs.
        """
        self.del_unit_numbers.make_map()
        self.ntv_pdfs.append(self.del_unit_numbers.map_file_name)


    def print_delinquent_units(self):
        """
        Prints a table of delinquent unit information stored in del_units.
        """
        os.system("cls")
        print("\n","-"*117,"\n",
              " #   Occupants", " "*51, "Guarantor", " "*31, "Balance Owed",
              "\n","-"*117, sep="")
        
        for unit_number, unit_information in self.del_units.items():
            print("{:>3}".format(unit_number) + ": ", end = "")
            unit_information.print_unit_information()


    def get_dates(self):
        """
        Obtains the notice and payment dates.

        Return:
            notice_date (str): The current date.
            due_date (str): The date three days from now, excluding 
                            weekends and recognized holidays.
        """
        os.system("cls")
        notice_date, due_date = DelDates.get_dates()
        return notice_date, due_date


    def write_delinquency_texts(self):
        """
        Writes an individual text for each unit. These 
        texts are to be sent to the residents of each unit 
        to make them aware of their outstanding balance.
        """
        del_texts = open(self.del_texts_file_name, "w")

        for unit in self.sorted_del_units:
            del_texts.write(unit.write_text_message())
        del_texts.close()
        print(f"Created {self.del_texts_file_name}")


    def prompt_for_delinquency_data(self):
        """
        Get delinquency report information from the 
        user and store it in del_data_file_name.
        """
        delinquency_file = open(self.del_data_file_name, "w")
        data = input("\nPaste the delinquency report information here:\n> ")

        delinquency_file.write(f"{data}\n")
        while data := input("> "):
            delinquency_file.write(f"{data}\n")
        delinquency_file.close()


    def store_delinquency_data(self):
        """
        Read delinquency report information from del_data_file_name and 
        assign each unit its own DelinquencyUnit class object. Store each 
        object in del_units and each unit number in del_unit_numbers.
        """                          
        delinquency_file = open(self.del_data_file_name, "r")             

        while line := (delinquency_file.readline()).split('\t'):    

            if line[0] != "*Apartment Name*":                 
                break
            name = line[3]                    

            if line[4] == "Guarantor" or line[4] == "": 
                self.del_units[self.back()].add_guarantor(name)      
                continue

            if line[4] == "Responsible":                            
                self.del_units[self.back()].add_occupant(name)
                continue               

            unit_number = int(line[1])                                 
            balance = line[11]
            self.del_units[unit_number] = DelUnit.DelUnit(name, 
                                                          unit_number, 
                                                          balance)
            self.del_unit_numbers.append_unit(unit_number)

        delinquency_file.close()


    def edit_delinquent_units(self):
        """
        Allows the user to edit information stored in del_units.
        """
        while True:
            print("Which unit number is incorrect?:")
            unit_to_edit = input("> ")
            if (unit_to_edit.isdigit() 
                    and int(unit_to_edit) in self.del_units.keys()):
                unit_to_edit = int(unit_to_edit)
                break
            print("Invalid unit number. Please try again.\n")

        os.system("cls")
        print(f"\nEditing unit {unit_to_edit}: ")

        while True:
            self.del_units[unit_to_edit].print_information_menu()
            edit_option = input("> ")

            if edit_option == "1":
                self.del_units[unit_to_edit].edit_occupants()
            elif edit_option == "2":
                self.del_units[unit_to_edit].edit_guarantor()
            elif edit_option == "3":
                self.del_units[unit_to_edit].edit_balance_owed()
            else:
                break


    def get_ntv_pdfs(self, notice_date, due_date):
        """
        Creates an individual NTV PDF for each delinquent 
        unit and combines them into a single document.

        Parameters:
            notice_date (str): The current date.
            due_date (str): The date three days from now, excluding 
                            weekends and recognized holidays.
        """
        for i, unit in enumerate(self.sorted_del_units):
            DelPDF.create_ntv_pdf(unit, notice_date, due_date, self.ntv_pdfs)
            print("+", end ="", flush=True)
            if not (i + 1) % 15 and i:
                print()

        MergePDF.combine_pdf_pages(self.ntv_pdfs, self.master_del_file_name)
        print(f"\nCreated {self.master_del_file_name}")


    def remove_pdfs(self):
        """
        Deletes all individual NTV PDFs.
        """
        for file in self.ntv_pdfs:
            os.remove(file)
        print("\nFiles deleted succesfully.")