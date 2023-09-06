from operations import BuildingWalk
from operations import KeyList
from operations import DelinquencyManager
from operations import ReletForm

print("|--------------------------------------|\n",
      "| Welcome to Leasing Specialist Helper |\n",
      "|--------------------------------------|\n", 
      sep = "")

while True:
    
    print("\n1. Building Walk",
          "\n2. Key List",
          "\n3. Delinquency Manager",
          "\n4. Relet Form",
          "\n5. Quit")
    menu_selection = input("> ")

    if menu_selection == "1":
        BuildingWalk.building_walk()

    elif menu_selection == "2":
        KeyList.key_list()

    elif menu_selection == "3":
        DelinquencyManager.delinquency_manager()

    elif menu_selection == "4":
        ReletForm.create_relet_form()

    else:
        break

print("\nThank you for using Leasing Specialist Helper.",
      "\nHave a great day! :)\n")