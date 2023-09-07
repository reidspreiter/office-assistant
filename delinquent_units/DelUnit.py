import re

class DelUnit:
    """
    A class representing a delinquent unit.

    Attributes:
        primary (str): The primary resident.
        initials (str): The primary resident's initials.
        occupants (str): All unit occupants.
        guarantor (str): All unit guarantors.
        unit_number (int): The unit number.
        address (str): The unit mailing address.
        balance (str): The balance the unit owes in number format. 
                       (1,000.00)
        balance_in_words (str): The balance the unit owes in word format.
                                (One Thousand & Two Dollars    23/100)
    """


    def __init__(self, primary, unit_number, balance):
        """
        Initializes a DelUnit object.

        Parameters:
            primary (str): The primary resident.
            unit_number (int): The unit number.
            balance (str): The balance the unit owes.
        """
        self.primary = self.format_name(primary)
        self.initials = self.format_initials()
        self.occupants = self.primary
        self.guarantor = "N/A"
        self.unit_number = unit_number
        self.address = self.format_address()
        self.balance = self.format_balance(balance)
        self.balance_in_words = self.format_balance_in_words(self.balance)


    def print_unit_information(self):
        """
        Prints occupants, guarantor, and balance.
        """
        print ("{:<60}".format(self.occupants), 
               "{:<40}".format(self.guarantor),
               "{:>8}".format(self.balance))
        
    
    def print_information_menu(self):
        """
        Prints occupants, guarantor, and 
        balance in a menu format.
        """
        print(f"\n1. Occupants: {self.occupants}",
              f"2. Guarantor: {self.guarantor}",
              f"3. Balance: {self.balance}",
              "4. Exit",
              sep="\n")
        
    
    def write_text_message(self):
        """
        Writes a delinquency text message.

        Return:
            (str): A text message.
        """
        return f"{self.unit_number}\nHi {self.primary.split()[0]}, this is\
 Reid with *APT*. I am reaching out because you have an outstanding balance of\
 ${self.balance} on your account. Are you able to get this paid today? Let me\
 know if you have any questions :)\n\n"


    def add_guarantor(self, guarantor):
        """
        Adds a guarantor for the unit.

        Parameter:
            guarantor (str): The name of a guarantor.
        """
        guarantor = self.format_name(guarantor)
        if self.guarantor == "N/A":
            self.guarantor = guarantor
        else:
            self.guarantor += f" and {guarantor}"


    def add_occupant(self, occupant):
        """
        Adds an occupant for the unit.

        Parameters:
            occupant (str): The name of an occupant.
        """
        occupant = self.format_name(occupant)
        self.occupants += f" and {occupant}"


    def edit_occupants(self):
        """
        Allows the user to edit the unit occupants.
        """
        print("Enter correct occupant information: ")
        self.occupants = input("> ")


    def edit_guarantor(self):
        """
        Allows the user to edit the unit's guarantors.
        """
        print("Enter correct guarantor information:")
        self.guarantor = input("> ")


    def edit_balance_owed(self):
        """
        Allows the user to edit the unit's balance.
        """
        while True:
            print("Enter correct balance information in numerical format:",
                  "\n(1,000.00, 100.00, 10.00, 1.00, 0.10, 0.01)")
            input_balance = input("> ")
            balance_pattern = "([1-9],)?[0-9]{1,3}(\.[0-9][0-9])$"
            if re.match(balance_pattern, input_balance):
                break
            print("Incorrect format. Please try again.\n")
        
        self.balance = input_balance
        self.balance_in_words = self.format_balance_in_words(self.balance)


    def format_name(self, name):
        """
        Reformats a name into "First Last" format.

        Parameters:
            name (str): A name passed in "Last, First" format.

        Return:
            (str): A name in "First Last" format.
        """
        #remove any parenthetical nicknames
        if name.find('(') != -1:                                                
            name = (name[ : name.index('(') : ] 
                    + name[name.index(')') + 1 : : ])

        first = (name.split(',')[1])[1:]                                 
        last = name.split(',')[0]                                             

        if first[-1] != ' ':                                                    
            first += ' '
        return first + last                                                     


    def format_initials(self):
        """
        Gets the primary residents initials.

        Return:
            (str): The primary resident's initials.
        """
        name = self.primary.split()
        return name[0][0] + name[1][0]


    def format_address(self):
        """
        Gets the correct address for a unit number.

        Return:
            (str): The unit's mailing address.
        """
        if self.unit_number < 101:
            return f"*Address 1* {self.unit_number}"
        return f"Address 2* {self.unit_number}"


    def format_balance(self, balance):
        """
        Ensures there is no whitespace at the end of balance.

        Parameters:
            balance (str): The unit's balance in number format.

        Return:
            (str): The unit's balance in number format.
        """
        return balance[:(balance.index('.') + 3)] 


    def format_balance_in_words(self, balance):
        """
        Format's the unit's balance in word format.

        Parameters:
            balance (str): The unit's balance in number format.

        Return:
            (str): The unit's balance in word format.
        """
        ones_digits = ["", "One ", "Two ", "Three ", "Four ", "Five ", 
                       "Six ", "Seven ", "Eight ", "Nine "]
        tens_digits = ["", "", "Twenty ", "Thirty ", "Forty ", "Fifty ", 
                       "Sixty ", "Seventy ", "Eighty ", "Ninety "]
        teen_digits = ["Ten", "Eleven ", "Twelve ", "Thirteen ", 
                       "Fourteen ", "Fifteen ", "Sixteen ", 
                       "Seventeen ", "Eighteen ", "Nineteen "]
        balance_in_words = ""

        if len(balance) == 8:
            balance_in_words += ones_digits[int(balance[0])] + "Thousand "
            balance = balance[2:]

        if len(balance) == 6:
            if balance[0] != '0':
                balance_in_words += ones_digits[int(balance[0])] + "Hundred "
            balance = balance[1:]

        if balance_in_words != "":
            balance_in_words += "& "

        if len(balance) == 5:
            if balance[0] == '1':
                balance_in_words += teen_digits[int(balance[1])]
                balance = balance[3:]
            else:
                balance_in_words += tens_digits[int(balance[0])]
                balance = balance[1:]

        if len(balance) == 4:
            balance_in_words += ones_digits[int(balance[0])]
            balance = balance[2:]
        
        # At this point, balance only stores the cent portion 
        # of the owed balance, and balance_in_words stores the rest.
        return balance_in_words + "Dollars     " + balance + "/100"