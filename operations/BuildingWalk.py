from unit_numbers import UnitNumbers


def building_walk():
    """
    Wrapper function for a series of UnitNumbers's methods that work 
    together to create a building walk map and a list of key codes.
    """
    unit_numbers_to_walk = UnitNumbers.UnitNumbers()
    unit_numbers_to_walk.populate(purpose="unit numbers to walk")
    unit_numbers_to_walk.sort_to_walk()

    print("Would you like an accompanying list of key codes? (y/n):")
    if input("> ") == "y":
        unit_numbers_to_walk.get_key_codes()
    unit_numbers_to_walk.make_map()
