import os
import fpdf

from unit_numbers import SortByBuilding
from unit_numbers import UnitCoordinates
from unit_numbers import KeyBox
from operations import MergePDF

class UnitNumbers:
    """
    A class representing a list of unit numbers.

    Attributes:
        unit_numbers (int list): A list of unit numbers.
        key_codes (str list): A list of key_codes. 
        map_file_name (str): The name to save a map file as.
    """


    def __init__(self, unit_numbers = None):
        """
        Initializes a UnitNumbers object.

        Parameters:
            unit_numbers (int list): An optional list of unit numbers.
        """
        if unit_numbers is None:
            self.unit_numbers = []
        else:
            self.unit_numbers = unit_numbers

        self.key_codes = []
        self.map_file_name = "Building Walk.pdf"


    def append_unit(self, unit_number):
        """
        Appends a unit number to unit_numbers.

        Parameters:
            unit_number (int): A unit number.
        """
        self.unit_numbers.append(unit_number)


    def empty(self):
        """
        Sets unit_numbers to an empty list.
        """
        self.unit_numbers = []


    def back(self):
        """
        Returns the last int in unit_numbers.
        """
        return self.unit_numbers[-1]
    

    def sort_ascending(self):
        """
        Sorts unit_numbers in ascending order.
        """
        self.unit_numbers.sort()


    def get_key_codes(self):
        """
        Populates the key_codes attribute with codes
        corresponding to unit_numbers and sorts them
        in ascending order based on letter and number.
        """
        for unit_number in self.unit_numbers:
            self.key_codes.append(KeyBox.key_box.get(unit_number))
        self.key_codes.sort(key=lambda x: (x[0], int(x[1:])))


    def print_key_codes(self):
        """
        Prints key_codes with specific formatting to
        place each letter group on its own line.
        """
        os.system("cls")
        print("Key Codes:")
        letter = self.key_codes[0][0]
        for key_code in self.key_codes:
            if key_code[0] != letter:
                letter = key_code[0]
                print()
            print(f"{key_code} ", end="")
        print()


    def populate(self, purpose):
        """
        Empties unit_numbers and populates it
        with new numbers entered by the user.

        Parameters:
            purpose (str): The purpose the user-entered 
                           unit numbers will serve.
        """
        while True:

            print(f"Collecting {purpose}.",
                  "\nEnter comma separated unit numbers to (1,48,30,111,...)")
            input_list = input("> ")
            input_list = input_list.split(",")
            invalid_units = []
            self.empty()

            for unit_number in input_list:
                try:
                    unit_number = int(unit_number)
                except ValueError:
                    invalid_units.append(unit_number)
                else:
                    if not (1 <= unit_number <= 72 or 
                            101 <= unit_number <= 140 or 
                            201 <= unit_number <= 260):
                        invalid_units.append(unit_number)

                    elif unit_number not in self.unit_numbers:
                        self.append_unit(unit_number)

            if not invalid_units:
                break
            print("\nThe following unit numbers were rejected:",
                f"\n{invalid_units}")
            print("The accepted unit numbers are as follows:",
                f"\n{self.unit_numbers}")
            print("\nPress 'Enter' to continue.", 
                "\nOr, press any key to enter a new list.")
            if input("> ") == "":
                break

        self.sort_ascending()


    def sort_to_walk(self):
        """
        Sorts unit_numbers in an order that 
        is most ideal to walk in real life.
        """
        split_buildings = SortByBuilding.sort_by_building(self.unit_numbers)
        self.empty()

        # This condition exists to reduce the complexity of 
        # the conditions inside the following for loops.
        if (bool(split_buildings[2]["front"]) 
            ^ bool(split_buildings[2]["back"])):
            split_buildings[3]["front"].reverse()

        direction = -1
        for building_number in split_buildings:
            for side, units in split_buildings[building_number].items():

                if not units:
                    continue

                if (building_number <= 4 
                        and side == "front" 
                        and units.reverse() != []):
                    split_buildings[building_number]["back"].reverse()

                elif building_number > 4:
                    if ((building_number % 2 and direction == -1) 
                            or (not building_number % 2 and direction == 1)):
                        units.reverse()
                    direction *= -1

                self.unit_numbers += units


    def make_map(self):
        """
        Plots and routes unit_numbers on 
        a map template pdf of the property.
        """
        template_file_name = "DO_NOT_DELETE_map_template.pdf"
        overlay_file_name = "temp_overlay.pdf"

        pdf = fpdf.FPDF(format = "letter", unit = "pt", orientation = "L")
        pdf.add_page()
        pdf.set_fill_color(255, 0, 0)
        pdf.set_draw_color(255, 0, 0)
        pdf.ellipse(x = 416, y = 372, w = 10, h = 10, style = "F")

        previous_coordinate = (416, 372)
        for unit_number in self.unit_numbers:
            current_coordinate = UnitCoordinates.unit_coordinates[unit_number]
            pdf.ellipse(x = current_coordinate[0], 
                        y = current_coordinate[1], 
                        w = 10, h = 10, style = "F")
            pdf.line(x1 = previous_coordinate[0] + 5, 
                     y1 = previous_coordinate[1] + 5, 
                     x2 = current_coordinate[0] + 5, 
                     y2 = current_coordinate[1] + 5)
            previous_coordinate = current_coordinate

        if self.key_codes:
            pdf.set_font("Arial", size = 7.9)
            pdf.set_text_color(0, 0, 0)
            pdf.set_xy(586, 25)
            pdf.cell(0, txt = "Key Codes:")

            x, y = 586, 35
            for i, key_code in enumerate(self.key_codes):
                if not i % 23 and i:
                    x += 25
                    y = 35
                pdf.set_xy(x, y)
                pdf.cell(0, txt = key_code)
                y += 10

        pdf.output(overlay_file_name)
        MergePDF.merge_pdfs(template_file_name, 
                            overlay_file_name, 
                            self.map_file_name)
        
        os.system("cls")
        print(f"Created {self.map_file_name}")
